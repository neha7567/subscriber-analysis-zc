import pandas as pd
import datetime
from subscriber_analysis.class_objects_to_df import find_num_workdays_in_month
import pickle

allocation_id_data = pd.read_pickle(
    'C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/subscriber_analysis/data_by_allocation_id')
subscriber_data = pd.read_pickle(
    "C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/subscriber_analysis/data_subscriber_details")


# create monthly dataset of subscribers active
def get_active_users_in_month(month_number, year_number):
    num_active_subscribers_each_month = {}
    num_new_subscribers_each_month = {}
    num_leaving_each_month = {}
    month_start_date = datetime.date(year_number, month_number, 1)

    # active_users_df = allocation_id_data[(allocation_id_data["actual_start"] < time_horizon_list[num_month + 1])
    # & (allocation_id_data["actual_end"] > time_horizon_list[num_month])]

    active_users_df = allocation_id_data[(allocation_id_data.actual_start.dt.date <= month_start_date) &
                                         (allocation_id_data.actual_end.dt.date > month_start_date)]

    num_active_subscribers_each_month[month_start_date] = active_users_df.shape[0]

    num_new_subscribers_each_month[month_start_date] = \
        allocation_id_data[(allocation_id_data["actual_start"].dt.month == month_number) &
                           (allocation_id_data.actual_start.dt.year == year_number)].shape[0]

    num_leaving_each_month[month_start_date] = \
        allocation_id_data[(allocation_id_data["actual_end"].dt.month == month_number)
                           & (allocation_id_data.actual_end.dt.year == year_number)].shape[0]
    return active_users_df, num_new_subscribers_each_month, num_new_subscribers_each_month, num_leaving_each_month


def get_earning_per_hour_df(month_num, year_num):
    start_date = datetime.date(year_num, month_num, 1)
    key_for_dict = start_date.strftime('%b-%Y')
    df_active_users = get_active_users_in_month(month_num, year_num)[0]

    df_active_users['weekday_hours_listed'] = 0
    df_active_users['weekend_hours_listed'] = 0
    df_active_users['earnings'] = 0

    for idx, row in df_active_users.iterrows():
        try:
            weekday_hours = row.monthly_listing_info[key_for_dict][2]
        except:
            weekday_hours = 0

        try:
            weekend_hours = row.monthly_listing_info[key_for_dict][3]
        except:
            weekend_hours = 0

        df_active_users.loc[idx, 'weekday_hours_listed'] = weekday_hours
        df_active_users.loc[idx, 'weekend_hours_listed'] = weekend_hours
        listed_hours = weekday_hours + weekday_hours

        try:
            earnings_on_this_zap_id = subscriber_data[subscriber_data.zap_id == row.zap_id].iloc[0]. \
                monthly_invoice_dict[key_for_dict][1]
        except:
            earnings_on_this_zap_id = 0
        df_active_users.loc[idx, 'earnings'] = earnings_on_this_zap_id

    df_active_users['total_subscribers_active'] = df_active_users.shape[0]
    df_active_users['num_cars_per_day_weekdays'] = get_mean_cars_weekdays_weekends_month(month_num, year_num)[0]
    df_active_users['num_cars_per_day_weekends'] = get_mean_cars_weekdays_weekends_month(month_num, year_num)[1]
    df_active_users['month'] = key_for_dict
    df_active_users['date'] = start_date

    return df_active_users


def get_mean_cars_weekdays_weekends_month(month_num, year_num):
    start_date = datetime.date(year_num, month_num, 1)
    key_for_dict = start_date.strftime('%b-%Y')
    df_active_users = get_active_users_in_month(month_num, year_num)[0]

    num_cars_weekdays = 0
    num_cars_weekends = 0
    for idx, row in df_active_users.iterrows():
        num_cars_weekdays += row.monthly_listing_info[key_for_dict][0]
        num_cars_weekends += row.monthly_listing_info[key_for_dict][1]

    mean_listed_cars_weekday_per_day = \
        num_cars_weekdays / (find_num_workdays_in_month(start_date)[0])

    mean_listed_cars_weekend_per_day = \
        num_cars_weekends / (find_num_workdays_in_month(start_date)[1])
    return mean_listed_cars_weekday_per_day, mean_listed_cars_weekend_per_day


start_of_horizon = datetime.date(2018, 1, 1)
end_of_horizon = datetime.date(2020, 2, 1)
time_horizon_list = pd.date_range(start_of_horizon, end_of_horizon, freq='MS').to_pydatetime()

df = pd.DataFrame()
for i in time_horizon_list:
    x = get_earning_per_hour_df(i.month, i.year)
    df = df.append(x, ignore_index=True)

pickle.dump(df, open('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/subscriber_analysis/data_subscriber_panel_data_for_regression','wb'))