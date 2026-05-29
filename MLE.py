import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

dataset = pd.read_csv('beijing_weather_30yr.csv',usecols=[0,1])
dataset['date'] = pd.to_datetime(dataset['date'])
dataset['year']=dataset['date'].dt.year
dataset['dayofyear']=dataset['date'].dt.dayofyear

def find_dashu_dates(dataset):
    dashu_rel_dates= [] 
    dashu_act_dates=[]
    for year,dataframe in dataset.groupby('year'):
        temps = dataframe['temp_avg'].values
        doys = dataframe['dayofyear'].values
        
        n_days = len(temps)
        current_sum = sum(temps[:15])
        max_sum = current_sum
        best_start = 0
        
        for j in range(1, n_days - 14):
            current_sum = current_sum - temps[j-1] + temps[j+14]
            if current_sum > max_sum:
                max_sum = current_sum
                best_start = j
                
        median= best_start + 7
        dashu_rel_dates.append(doys[median])
        dashu_act_dates.append(dataframe['date'].iloc[median].date())
    return dashu_rel_dates,dashu_act_dates

#shift the starting time of each year to June
#make winter (Dec and Jan) connected
def get_winter_year(date):
    if date.month<7:
        return date.year-1
    else:
        return date.year

def find_dahan_dates(dataset):
    dataset['winter_year']=dataset['date'].apply(get_winter_year)
    dahan_rel_dates=[]
    dahan_act_dates=[]
    for w_year, dataframe in dataset.groupby('winter_year'): 
        temps = dataframe['temp_avg'].values
        doys = dataframe['dayofyear'].values
        
        n_days = len(temps)
        current_sum = sum(temps[:15])
        min_sum = current_sum
        best_start = 0
        
        for j in range(1, n_days - 14):
            current_sum = current_sum - temps[j-1] + temps[j+14]
            if current_sum < min_sum:
                min_sum = current_sum
                best_start = j
                
        median= best_start + 7
        dahan_rel_dates.append(doys[median])
        dahan_act_dates.append(dataframe['date'].iloc[median].date())
    #discard 2023 data, for it only covers December
    dahan_rel_dates.pop()
    dahan_act_dates.pop()
    return dahan_rel_dates,dahan_act_dates


#find the hottest/ coldest period of each year 
#note the median date of this 15 days period
dashu_rel_dates,dashu_act_dates=find_dashu_dates(dataset)
dahan_rel_dates,dahan_act_dates=find_dahan_dates(dataset)


# fix the Dahan dates 
# december dates become negative not close to 300
for i,value in enumerate(dahan_rel_dates):
    if value >300:
        dahan_rel_dates[i]=value-365


#plot QQ plots
#check if the dates are normally distributed
def qq_plot(list,name):
    data = np.array(list)
    n = len(data)
    quantiles = (np.arange(1, n + 1) - 0.5) / n
    theoretical_quantiles = stats.norm.ppf(quantiles)
    sample_quantiles = np.sort(data)
    plt.figure()
    plt.scatter(theoretical_quantiles, sample_quantiles)
    plt.title('Q-Q Plot for {}'.format(name))
    plt.xlabel('theoretical quantiles (N(0,1))')
    plt.ylabel('sample quantiles (day of year)')

qq_plot(dashu_rel_dates,'Dashu')
qq_plot(dahan_rel_dates,'Dahan')

#Using MLE method, we can derive these equations
mean_ds_mle=np.mean(dashu_rel_dates)
mean_dh_mle=np.mean(dahan_rel_dates)
std_ds_mle=np.std(dashu_rel_dates)
std_dh_mle=np.std(dahan_rel_dates)
print(dahan_act_dates)
print(mean_ds_mle,std_ds_mle)
print(mean_dh_mle,std_dh_mle)

#derive the estimate actual dates from relative dates
estimate_ds_mle=dataset['date'].iloc[round(mean_ds_mle)]
estimate_dh_mle=dataset['date'].iloc[round(mean_dh_mle)]
print(estimate_ds_mle,estimate_dh_mle)

#Visualization
#plot histogram & gaussian fit by MLE
plt.figure()
plt.hist(dashu_rel_dates, bins=10, density=True)
xmin1, xmax1 = plt.xlim()
x1 = np.linspace(xmin1, xmax1, 100)
p1 = stats.norm.pdf(x1, mean_ds_mle, std_ds_mle)
plt.plot(x1, p1, label='MLE Gaussian Fit')
plt.title('Hottest period of year distribution')

plt.figure()
plt.hist(dahan_rel_dates, bins=10, density=True)
xmin2, xmax2 = plt.xlim()
x2 = np.linspace(xmin2, xmax2, 100)
p2 = stats.norm.pdf(x2, mean_dh_mle, std_dh_mle)
plt.plot(x2, p2, label='MLE Gaussian Fit')
plt.title('Coldest period of year distribution')
plt.show()