import numpy as np
import pandas as pd
import functions_lead_times_listing_booking as listing_functions
import statsmodels
import pickle
import datetime
import matplotlib.pyplot as plt

listing_data_reg_entire_pop = listing_functions.get_listing_regression_data()
listing_data_reg_entire_pop.to_csv("C:\\Users\\Neha Sharma\\Google "
                                   "Drive\\ZoomCar_data\\subscriber_data\\subscriber_listing_for_reg_1.csv")


listing_dataset_for_sub_group_reg, blah = listing_functions.get_data_for_listing_lead_times_for_sub_group_regression()
# creating pool of similar users - same start date and tenure greater than 6 months
data_for_pool_similar_users = listing_dataset_for_sub_group_reg[
    (listing_dataset_for_sub_group_reg.actual_start.dt.month == 1)
    & (listing_dataset_for_sub_group_reg.actual_start.dt.year == 2019)
    & (listing_dataset_for_sub_group_reg.actual_tenure < 24)
    & (listing_dataset_for_sub_group_reg.actual_tenure < 24)
    & (listing_dataset_for_sub_group_reg.city_id == 1)]

data_for_pool_similar_users['mean_listing_over_month_subs'] = \
    data_for_pool_similar_users.groupby('listing_month_year')['mean_listing_lead_time'].transform("mean")
new_df = data_for_pool_similar_users[['mean_listing_over_month_subs', 'listing_month_year']].drop_duplicates()
new_df['listing_month_year'] = pd.to_datetime(new_df['listing_month_year'], format='%b-%Y')
new_df.sort_values(by='listing_month_year', inplace=True)

plt.plot(new_df.listing_month_year, new_df.mean_listing_over_month_subs)
plt.show()
