import pandas as pd
import datetime


def clean_dataset(complete_data):
    complete_data = complete_data.rename(columns={"starts": "booking_starts", "ends": "booking_ends",
                                                  'created_at': 'booking_created_date'})
    complete_data.tenure_starts = pd.to_datetime(complete_data.tenure_starts, infer_datetime_format=True)
    complete_data.tenure_ends = pd.to_datetime(complete_data.tenure_ends, infer_datetime_format=True)
    complete_data.booking_created_date = pd.to_datetime(complete_data.booking_created_date, infer_datetime_format=True)
    complete_data.booking_starts = pd.to_datetime(complete_data.booking_starts, infer_datetime_format=True)
    complete_data.booking_ends = pd.to_datetime(complete_data.booking_ends, infer_datetime_format=True)
    complete_data.listing_starts = pd.to_datetime(complete_data.listing_starts, infer_datetime_format=True)
    complete_data.listing_ends = pd.to_datetime(complete_data.listing_ends, infer_datetime_format=True)
    complete_data.listing_created_at = pd.to_datetime(complete_data.listing_created_at, infer_datetime_format=True)
    complete_data['listing_lead_time'] = (complete_data.listing_starts -
                                          complete_data.listing_created_at).dt.total_seconds() / 3600
    complete_data['listing_length'] = (complete_data.listing_ends -
                                       complete_data.listing_starts).dt.total_seconds() / 3600
    complete_data['booking_length'] = (complete_data.booking_ends -
                                       complete_data.booking_starts).dt.total_seconds() / 3600
    complete_data['time_to_booking'] = (complete_data.booking_created_date -
                                        complete_data.listing_created_at).dt.total_seconds() / 3600
    return complete_data


def clean_listing_dataset(listing_data):
    listing_data.listing_starts = pd.to_datetime(listing_data.listing_starts, infer_datetime_format=True)
    listing_data.listing_ends = pd.to_datetime(listing_data.listing_ends, infer_datetime_format=True)
    listing_data.listing_created_at = pd.to_datetime(listing_data.listing_created_at, infer_datetime_format=True)
    return listing_data


def create_dataset_for_computing_matching_prob(listing_data, subscriber_booking_data, demand_data,
                                               JIT_hours, start_date, end_date):
    time_horizon_list = pd.date_range(start_date, end_date).to_pydatetime()

    early_listing, total_s, late_listing, early_demand, period_2_demand = [], [], [], [], []
    matched_in_p1, matched_in_p2, day_of_week, month = [], [], [], []
    for d in time_horizon_list:
        day_of_week.append(d.weekday()) # Monday is 0, Sunday is 6.
        month.append(str(d.strftime("%B")))
        s_1, s_2, sm1, sm2 = get_early_late_supply_on_a_date(listing_data, subscriber_booking_data, JIT_hours, d)
        d1, d2 = get_early_late_demand_on_a_date(demand_data, JIT_hours, d)
        early_listing.append(s_1), total_s.append(s_1 + s_2), late_listing.append(s_2), early_demand.append(d1), \
        period_2_demand.append(d2), matched_in_p1.append(sm1), matched_in_p2.append(sm2)

    data_set_for_prob = pd.DataFrame({'Date': time_horizon_list, 'Listed_P1': early_listing,
                                      'Total_S': total_s, 'Listed_P2': late_listing, 'Demand_P1': early_demand,
                                      'Demand_P2': period_2_demand, 'Matched_in_P1': matched_in_p1,
                                      'Matched_in_p2': matched_in_p2 , "day_of_week" : day_of_week,
                                      "month_name": month})

    return data_set_for_prob


def get_early_late_supply_on_a_date(data_listing, subscriber_with_bookings_data, JIT_hours, date):
    # date_plus = date + datetime.timedelta(days=1)
    # number who listed their cars
    total_supply_df = data_listing[(data_listing.listing_starts <= date) & (data_listing.listing_ends >= date)]
    total_supply_df['lead_time_this_date'] = (date - data_listing.listing_created_at).dt.total_seconds() / 3600
    # number available from this set of listing suppliers
    """booking_blocks_df = subscriber_with_bookings_data[(subscriber_with_bookings_data.booking_starts <= date) &
                                                      (subscriber_with_bookings_data.booking_ends >= date)]
    zap_id_na = booking_blocks_df['zap_id_x'].tolist()
    total_supply_df = total_supply_df[~total_supply_df['zap_id'].isin(zap_id_na)]"""

    early_supply_df = total_supply_df[total_supply_df.lead_time_this_date > JIT_hours]
    late_supply_df = total_supply_df[total_supply_df.lead_time_this_date <= JIT_hours]

    # matched in period 1
    total_bookings_this_day = subscriber_with_bookings_data[(subscriber_with_bookings_data.booking_starts <= date) &
                                                            (subscriber_with_bookings_data.booking_ends >= date)]
    total_bookings_this_day['booking_lead_time'] = (total_bookings_this_day.booking_starts -
                                                    total_bookings_this_day.booking_created_date).dt.total_seconds() / 3600
    early_bookings = total_bookings_this_day[total_bookings_this_day.booking_lead_time > JIT_hours]
    late_bookings = total_bookings_this_day[total_bookings_this_day.booking_lead_time <= JIT_hours]
    matched_early = early_bookings.shape[0]
    matched_late = late_bookings.shape[0]

    return early_supply_df.shape[0], late_supply_df.shape[0], matched_early, matched_late


def get_early_late_demand_on_a_date(demand_data, JIT_hours, date):
    # get all demand for that date, date is contained in start - end date list
    # date_plus = date + datetime.timedelta(days=1)
    inquiry_df = demand_data[(demand_data.actual_starts <= date) &
                             (demand_data.actual_ends >= date)]
    inquiry_df['lead_time_to_booking'] = (inquiry_df.actual_starts - inquiry_df.created_at).dt.total_seconds() / 3600
    return inquiry_df[inquiry_df.lead_time_to_booking > JIT_hours].shape[0], \
           inquiry_df[inquiry_df.lead_time_to_booking <= JIT_hours].shape[0]
