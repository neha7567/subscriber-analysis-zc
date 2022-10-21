import pandas as pd
import functions_for_cleaning_dataset as cleaning_fns
import numpy as np
import pickle
import datetime
import matplotlib.pyplot as plt

path = 'C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\ZoomCar_data\\subscriber_data\\'
booking_data_path = 'C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\ZoomCar_data\\booking_data\\'
start_of_horizon = datetime.date(2019, 1, 1)
end_of_horizon = datetime.date(2019, 12, 31)

subscriber_loc_details = pd.read_pickle(path + 'data_subscriber_details')
subscriber_data = pd.read_csv(path + 'subscriber_with_booking_id.csv')
bookings_2019_data = pd.read_pickle(booking_data_path + 'data_booking_2019')
listing_data = pd.read_csv(path + 'dim_listing_new.csv')
subscriber_data = subscriber_data.drop(['city', 'cargroup_id'], axis=1)
zaps_in_bangalore = subscriber_loc_details[subscriber_loc_details.city_name == 'Bangalore']['zap_id'].unique().tolist()

subscriber_data = pd.merge(left=subscriber_data, right=listing_data, left_on='id_listing', right_on='listing_id')
subscriber_data = pd.merge(left=subscriber_data, right=bookings_2019_data[['booking_id','city_id']], on='booking_id')

subscriber_data = subscriber_data[subscriber_data.city_id == 1]
listing_data = listing_data[listing_data['zap_id'].isin(zaps_in_bangalore)]

total_inquiry_data = pd.read_pickle('C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\ZoomCar_data\\'
                                    'inquiry_data_2019\\total_inquiry_data_2019')
total_inquiry_data = total_inquiry_data[total_inquiry_data.city == 'Bangalore']

subscriber_data = cleaning_fns.clean_dataset(subscriber_data)
listing_data = cleaning_fns.clean_listing_dataset(listing_data)

matching_prob_dataset = cleaning_fns.create_dataset_for_computing_matching_prob(listing_data, subscriber_data,
                                                                                total_inquiry_data, 48,
                                                                                start_of_horizon, end_of_horizon)
print(matching_prob_dataset.head())
#pickle.dump(matching_prob_dataset, open(path+'matching_prob_dataset_48', 'wb'))
matching_prob_dataset.to_csv(path+'matching_prob_dataset_48.csv')


matching_prob_dataset = cleaning_fns.create_dataset_for_computing_matching_prob(listing_data, subscriber_data,
                                                                                total_inquiry_data, 24,
                                                                                start_of_horizon, end_of_horizon)
print(matching_prob_dataset.head())
#pickle.dump(matching_prob_dataset, open(path+'matching_prob_dataset_24', 'wb'))
matching_prob_dataset.to_csv(path+'matching_prob_dataset_24.csv')





































#early_and_JIT_booking_supply(dataset, 48, start_of_horizon, end_of_horizon)




"""dataset.plot.scatter(x='listing_lead_time', y='time_to_booking')
plt.show()

dataset.plot.scatter(x='listing_length', y='time_to_booking')
plt.show()"""
