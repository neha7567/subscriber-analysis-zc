import pandas as pd
import pickle
import datetime
import calendar


class Utilities:

    @staticmethod
    def hours_from_start_of_day(date_time_1):
        x = (date_time_1 -
             datetime.datetime(date_time_1.year, date_time_1.month, date_time_1.day, 0, 0, 0)).total_seconds() / 3600
        return x

    @staticmethod
    def hours_to_end_of_day(date_time_1):
        x = (datetime.datetime(date_time_1.year, date_time_1.month, date_time_1.day, 23, 59, 59)
             - date_time_1).total_seconds() / 3600
        return x

    @staticmethod
    def get_dates_list_between_dates(date_time_1, date_time_2):  # get list of dates between two dates
        num_days = (date_time_2.date() - date_time_1.date()).days
        listed_dates_set = set()
        listed_dates_with_hours_dict = {}

        if num_days < 1:
            listed_dates_set.add(date_time_1.date())
            listed_dates_with_hours_dict[date_time_1.date()] = (date_time_2 - date_time_1).total_seconds() / 3600

        else:
            listed_dates_set.update([date_time_1.date(), date_time_2.date()])
            listed_dates_with_hours_dict[date_time_1.date()] = Utilities.hours_to_end_of_day(date_time_1)
            listed_dates_with_hours_dict[date_time_2.date()] = Utilities.hours_from_start_of_day(date_time_2)

            for i in range(1, num_days):
                key = date_time_1.date() + datetime.timedelta(days=i)
                listed_dates_with_hours_dict[key] = 24
                listed_dates_set.add(key)
        return listed_dates_set, listed_dates_with_hours_dict

    @staticmethod
    def get_weekday_weekends_days_hours_from_datedict(
            dates_as_keys_of_dict):  # from set of dates of listings in a month, get weekday_weekend dates
        weekday_days, weekend_days, weekday_hours, weekend_hours = 0, 0, 0, 0

        for date_iter in dates_as_keys_of_dict.keys():
            if Utilities.is_weekend(date_iter):
                weekend_days += 1
                weekend_hours += dates_as_keys_of_dict[date_iter]
            else:
                weekday_days += 1
                weekday_hours += dates_as_keys_of_dict[date_iter]
        return weekday_days, weekend_days, weekday_hours, weekend_hours

    @staticmethod
    def is_weekend(date):
        weekday_number = date.weekday()  # 5, 6 is Saturday Sunday
        if weekday_number < 5:
            return False
        else:
            return True


class Allocations:
    def __init__(self, allocation_id, car_id, zap_id, intended_start, intended_end, actual_start, actual_end,
                 subscription_fee, cargroup_name, location_id, city_name, offer_tag, offer_description
                 , cargroup_id, city_id, listing):
        self.allocation_id = allocation_id  # from data
        self.zap_id = zap_id  # from data
        self.car_id = car_id  # from data
        self.intended_start = intended_start  # from data
        self.intended_end = intended_end  # from data
        self.actual_start = actual_start  # from data
        self.actual_end = actual_end  # from data
        self.subscription_fee = subscription_fee  # from data
        self.cargroup_name = cargroup_name  # from data
        self.location_id = location_id  # from data
        self.city_name = city_name  # from data
        self.offer_tag = offer_tag  # from data
        self.offer_description = offer_description

        self.cargroup_id = cargroup_id  # derived
        self.city_id = city_id  # derived

        self.actual_tenure = (self.actual_end.year - self.actual_start.year) * 12 + \
                             (self.actual_end.month - self.actual_start.month)
        self.intended_tenure = (self.intended_end.year - self.intended_start.year) * 12 + \
                               (self.intended_end.month - self.intended_start.month)
        self.listing_info = listing

        self.listed_dates_with_hours_dict = {}
        self.monthly_listing_info = {}

        self.extract_listed_days_list()
        self.get_monthly_listing()

    def extract_listed_days_list(self):
        listed_days_set = set()
        listed_dates_with_hours_dict = {}
        for tuple_item in self.listing_info:
            tuple_dates_set, tuple_date_hour_dict = Utilities.get_dates_list_between_dates(tuple_item[0], tuple_item[1])
            listed_days_set.union(tuple_dates_set)
            intersection = set(listed_dates_with_hours_dict.keys()).intersection(set(tuple_date_hour_dict.keys()))
            for i in intersection:
                listed_dates_with_hours_dict[i] += tuple_date_hour_dict[i]
                del tuple_date_hour_dict[i]
            listed_dates_with_hours_dict.update(tuple_date_hour_dict)
        self.listed_dates_with_hours_dict = listed_dates_with_hours_dict

    def get_monthly_listing(self):
        starts = datetime.date(self.actual_start.year, self.actual_start.month, 1)
        ends = datetime.date(self.actual_end.year, self.actual_end.month,
                             calendar.monthrange(self.actual_end.year, self.actual_end.month)[1]) \
                             + datetime.timedelta(days=1) # end should not be inclusive when you do stuff with this
        date_ranges = pd.date_range(starts, ends,
                                    freq='MS').to_pydatetime()

        dictionary_monthly_listing_dic = {}
        for i in range(len(date_ranges) - 1):
            temp_dict = {k: v for k, v in self.listed_dates_with_hours_dict.items() if
                         date_ranges[i + 1].date() > k >= date_ranges[i].date()}  # filtered dictionary of this month.
            dictionary_monthly_listing_dic[date_ranges[i].strftime('%b-%Y')] = \
                Utilities.get_weekday_weekends_days_hours_from_datedict(temp_dict)
            # (num_weekdays, num_weekends, num_weekday_hours, num_weekend_hours)
        self.monthly_listing_info = dictionary_monthly_listing_dic

    def to_dict(self):
        return {
            'allocation_id': self.allocation_id, 'zap_id': self.zap_id, 'car_id': self.car_id,
            'intended_start': self.intended_start, 'intended_end': self.intended_end, 'actual_start': self.actual_start,
            'actual_end': self.actual_end, 'subscription_fee': self.subscription_fee,
            'cargroup_name': self.cargroup_name,
            'location_id': self.location_id, 'city_name': self.city_name, 'offer_tag': self.offer_tag,
            'offer_description':
                self.offer_description, 'cargroup_id': self.cargroup_id, 'city_id': self.city_id,
            'actual_tenure': self.actual_tenure, 'intended_tenure': self.intended_tenure,
            'monthly_listing_info': self.monthly_listing_info,
            'listed_dates_with_hours_dict': self.listed_dates_with_hours_dict
        }


class Subscriber:
    def __init__(self, zap_id, allocation_ids, monthly_payout_df,
                 city_name, city_id, cargroup_id, cargroup_name, location_id):
        self.zap_id = zap_id
        self.allocation_ids = allocation_ids
        self.monthly_payout_df = monthly_payout_df
        self.city_name = city_name
        self.city_id = city_id
        self.cargroup_id = cargroup_id
        self.cargroup_name = cargroup_name  # from data
        self.location_id = location_id  # from data
        self.monthly_invoice_dict = {}
        self.mean_subscription_fee = 0
        self.mean_net_fee = 0  # -ve implies owed to zoomcar
        self.mean_earnings = 0
        self.get_mean_payouts_for_user()

    def get_mean_payouts_for_user(self):
        user_payout_df = self.monthly_payout_df
        user_invoice_monthly_dic = {}
        for idx, row in user_payout_df.iterrows():
            user_invoice_monthly_dic[row['billing_cycle_start'].strftime('%b-%Y')] = \
                row['amount'], row['net_earnings'], row['net_subscription']

        self.mean_subscription_fee = user_payout_df['net_subscription'].mean()
        self.mean_net_fee = user_payout_df['amount'].mean()  # -ve implies owed to zoomcar
        self.mean_earnings = user_payout_df['net_earnings'].mean()
        self.monthly_invoice_dict = user_invoice_monthly_dic

    def to_dict(self):
        return {
            'zap_id': self.zap_id, 'allocation_ids': self.allocation_ids, 'cargroup_name': self.cargroup_name,
            'location_id': self.location_id, 'city_name': self.city_name, 'cargroup_id': self.cargroup_id,
            'city_id': self.city_id,
            'monthly_invoice_dict': self.monthly_invoice_dict, 'mean_subscription_fee': self.mean_subscription_fee,
            'mean_net_fee': self.mean_net_fee, 'mean_earnings': self.mean_earnings
        }
