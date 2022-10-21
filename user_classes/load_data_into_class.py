import pandas as pd
import pickle
import datetime

from user_classes.class_zap_users import Allocations, Subscriber

################################## load data into classes #####################################

invoice_data = pd.read_pickle('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/user_classes/data_invoice_by_zap_id')
listing_data = pd.read_pickle('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/user_classes/data_listing_by_allocation_id')
zap_users_data = pd.read_pickle('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/user_classes/data_zap_users_allocations')

################### store all objects as dictionary#######################################

subscribers = {}
allocations = {}

###########################################################################################

for index, row in zap_users_data.iterrows():
    if (row['tenure_starts']) < datetime.datetime(2020, 1, 1):
        print(row['tenure_starts'], row['tenure_ends'])
        actual_end = (row['tenure_ends']) if pd.isnull(row['allocation_actual_ends']) else (
            row['allocation_actual_ends'])

        listing = []  # get listing data as a tuple start_end time
        for ind, row_listing_data in listing_data[listing_data.allocation_id == row['allocation_id']].iterrows():
            print(row_listing_data['actual_starts'], row_listing_data['actual_ends'])
            listing.append((row_listing_data['actual_starts'], row_listing_data['actual_ends']))

        allocations[row['allocation_id']] = Allocations(row['allocation_id'], row['car_id'], row['zap_id'],
                                                        (row['tenure_starts']),
                                                        (row['tenure_ends']), (row['allocation_actual_starts']),
                                                        actual_end,
                                                        row['base_subscription_fee'], row['cargroup_name'],
                                                        row['location_id'],
                                                        row['city_name'], row['offer_tag_line'],
                                                        row['offer_description'],
                                                        row['cargroup_id'], row['city_id'], listing)

        print(allocations[row['allocation_id']].intended_tenure, allocations[row['allocation_id']].actual_tenure)

        ######### for subscriber class ####################

        allocations_ids = zap_users_data[zap_users_data.zap_id == row['zap_id']][
            'allocation_id'].unique()  # get allocation_ids attached to single zap user

        monthly_payout_df = invoice_data[invoice_data.zap_id == row['zap_id']]\
            [['net_subscription', 'net_earnings', 'amount', 'billing_cycle_start',
              'billing_cycle_end']]  # relevant dataframe for a zap_user

        subscribers[row['zap_id']] = Subscriber(row['zap_id'], allocations_ids, monthly_payout_df,
                                                row['city_name'],
                                                row['city_id'], row['cargroup_id'],
                                                row['cargroup_name'], row['location_id'])
        print(allocations_ids, monthly_payout_df)

pickle.dump(allocations, open('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/user_classes'
                              '/class_objects_zap_allocation_dictionary', 'wb'))
print('allocations_saved')
pickle.dump(subscribers, open('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/user_classes'
                              '/class_objects_subscriber', 'wb'))
print('subscriptions_saved')
