import pandas as pd


total_inquiry_data = pd.read_pickle('C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\ZoomCar_data\\'
                                    'inquiry_data_2019\\total_inquiry_data_2019')
total_inquiry_data = total_inquiry_data[total_inquiry_data.city == 'Bangalore']