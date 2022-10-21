import statsmodels.api as sm
import statsmodels.formula.api as smf
import datetime
import statsmodels
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import scipy.stats as stats

data = pd.read_pickle(
    'C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/subscriber_analysis/data_subscriber_panel_data_for_regression')
#data = data[data.actual_start < datetime.datetime(2019, 1, 1)]
data = data.dropna(axis=0, subset=['city_id', 'earnings'])
data['total_listed_hours'] = np.log(data['weekday_hours_listed'] + data['weekend_hours_listed'])
data['log_earnings'] = np.log(data['earnings'])
data['weekday_hours_listed'] = np.log(data['weekday_hours_listed'])
data['weekend_hours_listed'] = np.log(data['weekend_hours_listed'])
data['num_cars_per_day_weekends'] = np.log(data['num_cars_per_day_weekends'])
data['num_cars_per_day_weekdays'] = np.log(data['num_cars_per_day_weekdays'])
data = data.replace(-np.Inf, 0)
data['customer_type'] = data['subscription_fee'].apply(lambda row: 'low' if row < 25000 else 'high')
data = data.reset_index()

demean = lambda x: x - x.mean()
data_demeaned = data.groupby(by=['city_id']).transform(demean)[['weekday_hours_listed','weekend_hours_listed',
                                                                                             'total_listed_hours',
                                                                                             'total_subscribers_active',
                                                                                             'num_cars_per_day_weekdays',
                                                                                             'num_cars_per_day_weekends',
                                                                                             'log_earnings']]
data_demeaned['city_id'] = data['city_id']
data_demeaned['month'] = data['month']
data_demeaned['customer_type'] = data['customer_type']
data_demeaned = data_demeaned.reset_index()

scaler = StandardScaler()
scaled_data = pd.DataFrame(
    scaler.fit_transform(data_demeaned[['weekday_hours_listed', 'weekend_hours_listed',
                                        'total_listed_hours', 'total_subscribers_active', 'num_cars_per_day_weekdays',
                                        'num_cars_per_day_weekends', 'log_earnings']]),
    columns=['weekday_hours_listed', 'weekend_hours_listed', 'total_listed_hours',
             'total_subscribers_active', 'num_cars_per_day_weekdays',
             'num_cars_per_day_weekends', 'log_earnings'])

scaled_data['city_id'] = data_demeaned['city_id']
scaled_data['month'] = data_demeaned['month']
scaled_data['customer_type'] = data_demeaned['customer_type']
# scaled_data['date'] = df['date']
scaled_data.dropna(inplace=True)

model_ols = smf.ols(formula='(log_earnings) ~ weekday_hours_listed + num_cars_per_day_weekdays + C(customer_type)',
                    data=scaled_data).fit(cov_type='cluster', cov_kwds={'groups': scaled_data['city_id'].to_numpy()})
print(model_ols.summary())

residuals = model_ols.resid
fig = sm.qqplot(residuals, line='45')
plt.show()

sm.qqplot(residuals, stats.t, fit=True, line="45")
plt.show()

sm.graphics.plot_regress_exog(model_ols, 'weekday_hours_listed')
plt.show()

sm.graphics.plot_regress_exog(model_ols, 'num_cars_per_day_weekdays')
plt.show()

sm.graphics.plot_partregress_grid(model_ols)
plt.show()

sm.graphics.plot_leverage_resid2(model_ols)
plt.show()

sm.graphics.influence_plot(model_ols, criterion="cooks")
plt.show()

'''
mean_df = scaled_data.groupby(by='month').mean()
mean_df = mean_df.reset_index()
plt.scatter(mean_df.total_subscribers_active, mean_df.earnings, label="active_subscribers")
plt.scatter(mean_df.num_cars_per_day_weekdays, mean_df.earnings, label="num_cars_per_day_weekdays")
plt.scatter(mean_df.num_cars_per_day_weekends, mean_df.earnings, label="num_cars_per_day_weekends")
plt.legend()
plt.show()

for group, df in scaled_data.groupby(by=['month', 'city_id']):
    plt.scatter(df.weekday_hours_listed, df.earnings, label='weekday_listed_hours')
    plt.scatter(df.weekend_hours_listed, df.earnings, label='weekend_listed_hours')
    plt.legend()
    plt.title(f"{group}")
    plt.show()
'''
