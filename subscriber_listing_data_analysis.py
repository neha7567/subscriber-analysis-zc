import pandas as pd
import numpy as np
import pickle
import datetime
import matplotlib.pyplot as plt


allocation_id_data = pd.read_pickle('C:\\Users\\Neha Sharma\\Google '
                                    'Drive\\ZoomCar_data\\subscriber_data\\data_by_allocation_id')

allocation_id_data.head().to_string()
start_of_horizon = datetime.date(2018, 1, 1)
end_of_horizon = datetime.date(2020, 2, 1)
time_horizon_list = pd.date_range(start_of_horizon, end_of_horizon, freq='MS').to_pydatetime()

listing_df = pd.DataFrame()
for i in time_horizon_list:
    dict_key = i.strftime('%b-%Y')
    active_df = allocation_id_data[(allocation_id_data.actual_start.dt.date <= i.date()) &
                                   (allocation_id_data.actual_end.dt.date > i.date())]
    df = pd.DataFrame()
    for index, row in active_df.iterrows():
        df.loc[index, 'actual_tenure'] = row.actual_tenure
        df.loc[index, 'intended_tenure'] = row.intended_tenure
        try:
            df.loc[index, 'weekdays_listed'] = row.monthly_listing_info[dict_key][0]
            df.loc[index, 'weekends_listed'] = row.monthly_listing_info[dict_key][1]
        except:
            print('exception_occured')
            df.loc[index, 'weekdays_listed'] = 0
            df.loc[index, 'weekends_listed'] = 0
    df['month'] = i
    listing_df = listing_df.append(df, ignore_index=True)

listing_df['total_days_listed'] = listing_df['weekdays_listed'] + listing_df['weekends_listed']

num_listers = pd.DataFrame(columns=['month', 'never_listers', 'always_listers'])
i = 0
for group, dataframe in listing_df.groupby(by='month'):
    num_listers.loc[i] = [group, dataframe[dataframe.total_days_listed == 0].shape[0] / dataframe.shape[0],
                          dataframe[dataframe.total_days_listed >= 25].shape[0] / dataframe.shape[0]]
    i += 1

num_listers = num_listers.sort_values(by='month')
plt.plot(num_listers.month, num_listers.never_listers, label='Never list')
plt.plot(num_listers.month, num_listers.always_listers, label='List everyday')
# plt.title('listing_trend')
plt.xlabel('Month year', fontsize=40)
plt.ylabel('% of subscribers', fontsize=40)
plt.locator_params(axis='x', nbins=5)
plt.xticks(fontsize=34)
plt.yticks(fontsize=34)
plt.tight_layout()
plt.legend(prop={'size': 30})
plt.show()

'''
early_leavers = listing_df[listing_df.actual_tenure < listing_df.intended_tenure]
num_listers = pd.DataFrame(columns=['month', 'never_listers', 'always_listers'])
i = 0
for group, dataframe in early_leavers.groupby(by='month'):
    num_listers.loc[i] = [group, dataframe[dataframe.total_days_listed == 0].shape[0] / dataframe.shape[0],
                          dataframe[dataframe.total_days_listed >= 25].shape[0] / dataframe.shape[0]]
    i += 1

num_listers = num_listers.sort_values(by='month')
plt.plot(num_listers.month, num_listers.never_listers, label='never_listers')
plt.plot(num_listers.month, num_listers.always_listers, label='always_listers')
plt.title('early_leavers_lsiting_trend')
plt.xticks(fontsize=34)
plt.yticks(fontsize=34)
plt.tight_layout()
plt.legend(prop={'size': 30})
plt.show()

timely_leavers = listing_df[listing_df.actual_tenure == listing_df.intended_tenure]
num_listers = pd.DataFrame(columns=['month', 'never_listers', 'always_listers'])
i = 0
for group, dataframe in timely_leavers.groupby(by='month'):
    num_listers.loc[i] = [group, dataframe[dataframe.total_days_listed == 0].shape[0] / dataframe.shape[0],
                          dataframe[dataframe.total_days_listed >= 25].shape[0] / dataframe.shape[0]]
    i += 1

num_listers = num_listers.sort_values(by='month')
plt.plot(num_listers.month, num_listers.never_listers, label='never_listers')
plt.plot(num_listers.month, num_listers.always_listers, label='always_listers')
plt.title('planned_leavers_listing_trend')
plt.xticks(fontsize=34)
plt.yticks(fontsize=34)
plt.tight_layout()
plt.legend(prop={'size': 30})
plt.show()
'''

subscriber_reg_data = pd.read_pickle('C:\\Users\\Neha Sharma\\Google Drive\\'
                                     'ZoomCar_data\\subscriber_data\\data_subscriber_panel_data_for_regression')


month_start, num_active_subs, listed_cars_weekday, listed_cars_weekend, city_id, \
total_earnings, avg_earning = [], [], [], [], [], [], []

for group, monthly_data in subscriber_reg_data.groupby(by=['date']):
    for city, monthly_city_data in monthly_data.groupby(by='city_id'):
        month_start.append(group)
        num_active_subs.append(monthly_city_data.total_subscribers_active.iloc[0])
        listed_cars_weekend.append(monthly_city_data.num_cars_per_day_weekends.iloc[0])
        listed_cars_weekday.append(monthly_city_data.num_cars_per_day_weekdays.iloc[0])
        city_id.append(city)
        total_earnings.append(monthly_city_data.earnings.sum())
        avg_earning.append(monthly_city_data.earnings.sum()/monthly_city_data.total_subscribers_active.iloc[0])


data_of_interest = pd.DataFrame({'start_date_month': month_start, 'active_subscribers': num_active_subs,
                                 'total_cars_weekday': listed_cars_weekday, 'total_cars_weekend': listed_cars_weekend,
                                 'city_id': city_id, 'total_earnings_subscribers': total_earnings,
                                 'average_earning_subscriber': avg_earning})

pickle.dump(data_of_interest, open('C:\\Users\\Neha Sharma\\Google Drive\\'
                                     'ZoomCar_data\\subscriber_data\\data_subscriber_for_plots', 'wb'))

data_of_interest = data_of_interest.sort_values(by='start_date_month')
df_bangalore = data_of_interest[data_of_interest.city_id == 1]
plt.plot(df_bangalore.start_date_month, df_bangalore.active_subscribers, label='number_subscribers')
plt.plot(df_bangalore.start_date_month, df_bangalore.total_earnings_subscribers/1000, label= 'total_revenue')
plt.plot(df_bangalore.start_date_month, df_bangalore.average_earning_subscriber, label = 'average_earning')
#plt.plot(df_bangalore.start_date_month, df_bangalore.total_cars_weekday, label='total_cars_weekday')
#plt.plot(df_bangalore.start_date_month, df_bangalore.total_cars_weekend, label='total_cars_weekend')
plt.xlabel('month', fontsize=40)
plt.ylabel('revenue', fontsize=40)
plt.xticks(fontsize=34)
plt.yticks(fontsize=34)
plt.tight_layout()
plt.legend(prop={'size': 30})
plt.show()


