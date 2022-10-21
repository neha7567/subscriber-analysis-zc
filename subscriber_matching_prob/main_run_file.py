import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf

path_csv_files = 'C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\ZoomCar_data\\subscriber_data\\'
file_jit_48 = 'matching_prob_dataset_48.csv'
file_jit_24 = 'matching_prob_dataset_24.csv'

data_set = pd.read_csv(path_csv_files + file_jit_48)
data_set["ratio_period_p1"] = data_set["Listed_P1"]/data_set["Total_S"]
data_set['total_demand'] = data_set["Demand_P1"] + data_set['Demand_P2']
data_set["theta"] = data_set["Demand_P1"]/data_set["total_demand"]

fig, axs = plt.subplots()
axs.plot(data_set.theta, label="early proportion")
axs.plot(data_set.ratio_period_p1, label = "early_supply")
plt.legend()
plt.show()

fig, axs = plt.subplots(1, 2)
data_set.groupby('month_name')['ratio_period_p1'].plot(legend=True, ax=axs[0])
plt.ylabel("beta")
data_set.groupby('month_name')['theta'].plot(legend=True, ax = axs[1])
plt.ylabel("theta")
plt.show()

"""data_set.groupby('month_name')['theta'].plot(legend=True, ax = axs[1])
plt.ylabel("theta")
plt.show()"""

data_set.groupby("day_of_week")["ratio_period_p1"].plot(legend=True)
plt.ylabel("beta")
data_set.groupby("day_of_week")['theta'].plot(legend=True)
plt.ylabel("theta")
plt.show()


#plt.show()



# stat_test_supply = adfuller(data_set.Total_S)
stat_test_demand = adfuller(data_set.Demand_P1)
"""print(f'ADF Statistic: {stat_test_supply[0]}')
print(f'p-value: {stat_test_supply[1]}')
print(f'Demand data ADF Statistic: {stat_test_demand[0]}')
print(f'demand data p-value: {stat_test_demand[1]}')"""

total_s_dif = np.diff(data_set.Total_S, n=1)
stat_test_supply = adfuller(total_s_dif)
"""print(f'ADF Statistic: {stat_test_supply[0]}')
print(f'p-value: {stat_test_supply[1]}')"""


plot_acf(total_s_dif, lags=30)
plt.tight_layout()
plt.show()
plot_acf(data_set.Demand_P1, lags=30)
plt.tight_layout()
plt.show()


# fig, axs = plt.subplots(4, 3, sharey=False, sharex=True)