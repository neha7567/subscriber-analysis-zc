import pandas as pd
import pickle
import matplotlib.pyplot as plt
import datetime
import calendar

############load_data#############################################################
user_class_path = 'C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/user_classes/'
primary_demand_path = 'C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/Primary_demand/'
drive_path = 'C:/Users/Neha Sharma/Google Drive/ZoomCar_data/'

class_object_allocation = pickle.load(open(user_class_path + 'class_objects_zap_allocation_dictionary', 'rb'))
class_objects_subscriber = pickle.load(open(user_class_path + 'class_objects_subscriber', 'rb'))

zap_payout = pd.read_csv(drive_path + 'fact_zap_payout_new.csv')
zap_payout['billing_cycle_start'] = pd.to_datetime(zap_payout.billing_cycle_start, infer_datetime_format=True).dt.date \
                                    + datetime.timedelta(days=1)

bookings = pd.read_pickle(primary_demand_path + 'data_booking_2018')
bookings = pd.concat([bookings, pd.read_pickle(primary_demand_path + 'data_booking_2019')])


#####################################################################################

########################function################################################
def find_num_workdays_in_month(date_1):
    cal = calendar.Calendar()
    working_days = len([i for i in cal.itermonthdays2(date_1.year, date_1.month) if i[0] != 0 and i[1] < 5])
    total_days = calendar.monthrange(date_1.year, date_1.month)[1]
    weekends = total_days - working_days
    return working_days, weekends


############################################################################################


def get_listing_user_rev_stats():
    for num_month in range(len(time_horizon_list) - 1):
        active_users_df = allocation_id_data[(allocation_id_data["actual_start"] < time_horizon_list[num_month + 1])
                                             & (allocation_id_data["actual_end"] > time_horizon_list[num_month])]

        num_active_subscribers_each_month[time_horizon_list[num_month]] = active_users_df.shape[0]

        num_new_subscribers_each_month[time_horizon_list[num_month]] = \
            allocation_id_data[(allocation_id_data["actual_start"].dt.month == time_horizon_list[num_month].month) &
                               (allocation_id_data.actual_start.dt.year == time_horizon_list[num_month].year)].shape[0]

        num_leaving_each_month[time_horizon_list[num_month]] = \
            allocation_id_data[(allocation_id_data["actual_end"].dt.month == time_horizon_list[num_month].month)
                               & (allocation_id_data.actual_end.dt.year == time_horizon_list[num_month].year)].shape[
                0]
        df = allocation_id_data[(allocation_id_data.actual_start.dt.date <= time_horizon_list[num_month].date()) &
                                (allocation_id_data.actual_end.dt.date > time_horizon_list[num_month].date())]

        verification_data[time_horizon_list[num_month]] = df.shape[0]

        a = 0
        for idx, row in df.iterrows():
            try:
                listed_hours = \
                    row.monthly_listing_info[time_horizon_list[num_month].strftime('%b-%Y')][2] + \
                    row.monthly_listing_info[time_horizon_list[num_month].strftime('%b-%Y')][3]
            except:
                listed_hours = 0

            if listed_hours > 0:
                try:
                    earnings_per_hour = subscriber_data[subscriber_data.zap_id == row.zap_id].iloc[0]. \
                                            monthly_invoice_dict[time_horizon_list[num_month].strftime('%b-%Y')][
                                            1] / listed_hours
                except:
                    earnings_per_hour = 0

            else:
                earnings_per_hour = 0

            a += earnings_per_hour
        try:
            earning_per_listed_hour_each_month[time_horizon_list[num_month]] = a / df.shape[0]
        except:
            earning_per_listed_hour_each_month[time_horizon_list[num_month]] = 0

        num_cars_weekdays = 0
        num_cars_weekends = 0
        for idx, row in df.iterrows():
            num_cars_weekdays += row.monthly_listing_info[time_horizon_list[num_month].strftime('%b-%Y')][0]
            num_cars_weekends += row.monthly_listing_info[time_horizon_list[num_month].strftime('%b-%Y')][1]

        mean_listed_cars_weekday_each_month[time_horizon_list[num_month]] = \
            num_cars_weekdays / (find_num_workdays_in_month(time_horizon_list[num_month])[0])

        mean_listed_cars_weekend_each_month[time_horizon_list[num_month]] = \
            num_cars_weekends / (find_num_workdays_in_month(time_horizon_list[num_month])[1])

        bookings_data_df = bookings[bookings.actual_starts.dt.month == time_horizon_list[num_month].month]
        total_revenue_each_month[time_horizon_list[num_month]] = bookings_data_df.booking_fee.sum()
        weekday_demand_count_each_month[time_horizon_list[num_month]] = \
            bookings_data_df[bookings_data_df.is_weekend == False].shape[0]
        weekend_demand_count_each_month[time_horizon_list[num_month]] = \
            bookings_data_df[bookings_data_df.is_weekend == False].shape[0]


# get_listing_user_rev_stats()


if __name__ == "__main__":
    ### convert_class_objects to df####################################################
    allocation_id_data = pd.DataFrame.from_records(
        [class_object_allocation[s].to_dict() for s in class_object_allocation.keys()])
    subscriber_data = pd.DataFrame.from_records(
        [class_objects_subscriber[s].to_dict() for s in class_objects_subscriber.keys()])

    pickle.dump(allocation_id_data,
                open('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/subscriber_analysis'
                     '/data_by_allocation_id', 'wb'))
    pickle.dump(subscriber_data, open('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/subscriber_analysis'
                                      '/data_subscriber_details', 'wb'))

    ###################################################################################

    ######################define time horizon################################

    start_of_horizon = datetime.date(2018, 1, 1)
    end_of_horizon = datetime.date(2020, 2, 1)
    time_horizon_list = pd.date_range(start_of_horizon, end_of_horizon, freq='MS').to_pydatetime()

    ############################################################################

    #################define global variables######################################################
    total_revenue_each_month, weekday_demand_count_each_month, weekend_demand_count_each_month = {}, {}, {}
    num_active_subscribers_each_month, num_new_subscribers_each_month, num_leaving_each_month = {}, {}, {}
    earning_per_listed_hour_each_month, mean_listed_cars_weekday_each_month, mean_listed_cars_weekend_each_month = {}, {}, {}

    verification_data = {}

    get_listing_user_rev_stats()

    # print(num_subscribers_each_month, num_joined, num_left)
    total_users = sorted(num_active_subscribers_each_month.items())
    verification_users = sorted(verification_data.items())
    total_left = sorted(num_leaving_each_month.items())
    total_joined = sorted(num_new_subscribers_each_month.items())
    mean_payouts = sorted(earning_per_listed_hour_each_month.items())
    cars_weekday = sorted(mean_listed_cars_weekday_each_month.items())
    cars_weekend = sorted(mean_listed_cars_weekend_each_month.items())
    total_rev = sorted(total_revenue_each_month.items())
    total_weekend_bookings = sorted(weekend_demand_count_each_month.items())
    total_weekday_bookings = sorted(weekday_demand_count_each_month.items())

    month, total = zip(*total_users)
    month, left = zip(*total_left)
    month, joined = zip(*total_joined)
    month, payout = zip(*mean_payouts)
    month, weekday = zip(*cars_weekday)
    month, weekend = zip(*cars_weekend)
    month, rev = zip(*total_rev)
    month, num_weekday = zip(*total_weekday_bookings)
    month, num_weekend = zip(*total_weekend_bookings)
    month, verified = zip(*verification_users)

    plt.plot(month, total, label='total')
    plt.plot(month, left, label='left')
    plt.plot(month, joined, label='joined')
    plt.plot(month, verified, label='verified')
    # plt.plot(month, payout, label='average_earnings')
    plt.legend()
    plt.show()

    plt.plot(month, payout, label='average_earnings')
    plt.legend()
    plt.show()

    plt.plot(month, weekday, label='weekday_cars')
    plt.plot(month, weekend, label='weekend_cars')
    plt.legend()
    plt.show()

    plt.plot(month, rev, label='revenue')
    plt.plot(month, num_weekday, label='num_weekday')
    plt.plot(month, num_weekend, label='num_weekend')
    plt.legend()
    plt.show()

    plt.hist(allocation_id_data.intended_tenure, label='intended_tenure', alpha=0.50)
    plt.hist(allocation_id_data.actual_tenure, label='actual_tenure', alpha=0.50)
    plt.legend()
    plt.show()

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(month, payout, label='average_earnings')
    axs[0].legend()
    axs[1].plot(month, verified, label='verified')
    axs[1].legend()
    plt.show()
