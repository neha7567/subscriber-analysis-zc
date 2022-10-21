import numpy as np
import pandas as pd
import functions_lead_times_listing_booking as listing_functions
# import Primary_demand.clean_booking_data as cleaning_bookings_functions
import statsmodels
import pickle
import datetime
import matplotlib.pyplot as plt

"""inquiry_data = []
months = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'august', 'sept', 'oct', 'nov', 'dec']
for i in months:
    inquiry_data.append(pd.read_pickle('C:\\Users\\Neha Sharma\\Google '
                                       'Drive\\ZoomCar_data\\inquiry_data_2019\\data_inquiries_%s_2019' % i))

inquiry_data = pd.concat(inquiry_data)
pickle.dump(inquiry_data, open('total_inquiry_data_2019', 'wb'))"""

total_inquiry_data = pd.read_pickle('C:\\Users\\Neha Sharma\\Google '
                                    'Drive\\ZoomCar_data\\inquiry_data_2019\\total_inquiry_data_2019')

data = total_inquiry_data.head(n=100)
print(data)
