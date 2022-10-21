import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import Primary_demand.clean_booking_data as function_clean_booking


def clean_listing_data(data):
    data.dropna(subset=['listing_created_at', 'actual_starts', 'actual_ends', 'allocation_id'], inplace=True)
    data['listing_created_at'] = pd.to_datetime(data.listing_created_at, infer_datetime_format=True, errors='coerce')
    data['actual_starts'] = pd.to_datetime(data.actual_starts, infer_datetime_format=True, errors='coerce')
    data['actual_ends'] = pd.to_datetime(data.actual_ends, infer_datetime_format=True, errors='coerce')
    data['created_date'] = pd.to_datetime(data.listing_created_at.dt.date)
    data['listing_length'] = (data.actual_ends - data.actual_starts).dt.total_seconds() / 3600
    data['listing_lead_time'] = (data.actual_starts - data.listing_created_at).dt.total_seconds() / 3600
    data['listing_month_year'] = data.created_date.dt.strftime('%b-%Y')
    return data


def get_listing_regression_data():
    blah, listing_data_for_reg = get_data_for_listing_lead_times_for_sub_group_regression()
    listing_data_for_reg['time_in_zc'] = (listing_data_for_reg.listing_created_at - listing_data_for_reg.actual_start
                                          ).dt.total_seconds() / 3600
    listing_data_for_reg['listing_start_month'] = listing_data_for_reg.actual_starts.dt.month
    return listing_data_for_reg[['allocation_id', 'listing_lead_time', 'listing_length', 'listing_start_month',
                                 'city_name', 'city_id', 'time_in_zc', 'subscription_fee', 'is_weekend']]


def get_data_for_listing_lead_times_for_sub_group_regression():
    allocation_id_data = pd.read_pickle('C:\\Users\\Neha Sharma\\Google '
                                        'Drive\\ZoomCar_data\\subscriber_data\\data_by_allocation_id')

    listing_data = pd.read_csv('C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\dim_listing.csv')
    listing_data = clean_listing_data(listing_data)
    listing_data['is_weekend'] = listing_data.apply(function_clean_booking.is_weekend_demand, axis=1)
    listing_data['mean_listing_lead_time'] = listing_data.groupby(by=['listing_month_year',
                                                                 'allocation_id'])['listing_lead_time'].transform("mean")

    listing_with_unique_vals = listing_data[
        ['mean_listing_lead_time', 'listing_month_year', 'allocation_id', 'is_weekend']].drop_duplicates(
        subset=['mean_listing_lead_time', 'listing_month_year'], keep='first', inplace=False)

    new_data_set_with_listing_info = pd.merge(
        allocation_id_data[['allocation_id', 'actual_start', 'actual_end', 'subscription_fee', 'city_name',
                            'city_id', 'actual_tenure']], listing_with_unique_vals, how='inner', on='allocation_id')

    listing_data_with_allocation_info = pd.merge(
        allocation_id_data[['allocation_id', 'actual_start', 'actual_end', 'subscription_fee', 'city_name',
                            'city_id', 'actual_tenure', 'subscription_fee']], listing_data, how='inner', on='allocation_id')

    return new_data_set_with_listing_info, listing_data_with_allocation_info


if __name__ == "__main__":
    listing_data = pd.read_csv('C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\dim_listing.csv')
    booking_2019 = pd.read_pickle(
        'C:\\Users\\Neha Sharma\\PycharmProjects\\ZC_inquiry_by_pincode\\Primary_demand\\data_booking_2019')
    booking_2018 = pd.read_pickle(
        'C:\\Users\\Neha Sharma\\PycharmProjects\\ZC_inquiry_by_pincode\\Primary_demand\\data_booking_2018')
    total_booking_data = pd.concat([booking_2018, booking_2019], ignore_index=True)
    total_booking_data['inquiry_month_year'] = total_booking_data.created_at.dt.strftime('%b-%Y')
    listing_data = clean_listing_data(listing_data)


    def find_lead_time_patterns_for_time_horizon(horizon):
        mean_lead_time_bookings, mean_lead_time_listing, month_year_axis = [], [], []
        for given_date in time_horizon:
            month_year = given_date.strftime('%b-%Y')
            booking_df = total_booking_data[total_booking_data.inquiry_month_year == month_year]
            listing_df = listing_data[listing_data.listing_month_year == month_year]
            mean_lead_time_bookings.append(booking_df.lead_time.mean())
            mean_lead_time_listing.append(listing_df.listing_lead_time.mean())
            month_year_axis.append(month_year)
        return mean_lead_time_bookings, mean_lead_time_listing, month_year_axis


    time_horizon = pd.date_range('2018-01-01', '2020-1-1', freq='MS').to_pydatetime()
    mean_lead_time_bookings, mean_lead_time_listing, x_axis = find_lead_time_patterns_for_time_horizon(time_horizon)

    plt.plot(x_axis, mean_lead_time_bookings, label='mean_lead_times_bookings')
    plt.plot(x_axis, mean_lead_time_listing, label='mean_lead_time_listing')
    plt.legend()
    plt.show()


    def find_booking_lengths_patterns_for_time_horizon(horizon):
        mean_booking_lengths, mean_listing_lengths, month_year_axis = [], [], []
        for given_date in time_horizon:
            month_year = given_date.strftime('%b-%Y')
            booking_df = total_booking_data[total_booking_data.inquiry_month_year == month_year]
            listing_df = listing_data[listing_data.listing_month_year == month_year]
            mean_booking_lengths.append(booking_df.booking_length.mean())
            mean_listing_lengths.append(listing_df.listing_length.mean())
            month_year_axis.append(month_year)
        return mean_booking_lengths, mean_listing_lengths, month_year_axis


    time_horizon = pd.date_range('2018-01-01', '2020-1-1', freq='MS').to_pydatetime()
    mean_booking_lengths, mean_listing_lengths, x_axis = find_booking_lengths_patterns_for_time_horizon(time_horizon)

    # plt.plot(x_axis, mean_booking_lengths, label='mean_booking_lengths')
    plt.plot(x_axis, mean_listing_lengths, label='mean_listing_lengths')
    plt.legend()
    plt.show()


