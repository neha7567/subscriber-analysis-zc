import pandas as pd
import pickle
import numpy as np



################# create dictionary wioth city as keys and hubs in it as values.###############
hubs_data = pd.read_csv('C:/Users/Neha Sharma/hub_data.csv')
hubs_dict = {i : [] for i in hubs_data.city_id.unique()}
for i in hubs_dict.keys():
    hubs_dict[i] = hubs_data[hubs_data.city_id==i]['id'].unique()

pickle.dump(hubs_dict,open('city_hub_mapping_dict','wb'))


############################## all cargroup_ids with thier names and the car_types ids and cartype names and seating information#
######## This is each car and its characteristics(only seating)##########################

car_group_data = pd.read_csv('C:/Users/Neha Sharma/cargroups_202101141449.csv')
car_group_data = car_group_data[['id','name', 'seating', 'cartype','display_name']]
car_group_data = car_group_data.drop_duplicates()
car_group_data = car_group_data.rename(columns={"id": "cargroup_id", "name": "cargroup_name", 'display_name':'cargroup_display_name'})

cartype_data = pd.read_csv('C:/Users/Neha Sharma/car_types_202101141619.csv')

car_group_data = pd.merge(left = car_group_data,
                          right = cartype_data[['id','name']]
                          , left_on= 'cartype', right_on= 'id', how='left')

car_group_data = car_group_data.rename(columns={'cartype':'cartype_id', 'name':'cartype_name', 'seating':'num_seats'})
car_group_data = car_group_data.drop(['id'], axis=1)

pickle.dump(car_group_data, open('cargroup_and_type_map_df','wb'))


#############################city ids and their names#######

data = pd.read_pickle('C:/Users/Neha Sharma/PycharmProjects/ZC_inquiry_by_pincode/loc_data')
city_data = pd.read_csv('C:/Users/Neha Sharma/Google Drive/ZoomCar_data/useful_data/cities.csv')
city_data = city_data[['id','name']]
city_data = city_data.rename(columns={'id': 'city_id', 'name': 'city_name'})
data = pd.merge(data, city_data, how='left', on='city_id')

pickle.dump(city_data, open('city_id_name_map','wb'))# city name and id#
pickle.dump(data, open('locations_data','wb')) # location id, hub id, pincode, lat long of the location id, address, city id, city name.

#######################################################################################################