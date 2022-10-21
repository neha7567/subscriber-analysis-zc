import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np
from mpl_toolkits.mplot3d import axes3d
from math import factorial as fact
import operator as op
from functools import reduce


path = 'C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\subscriber_data\\'


def compute_combs(n, r):
    if n - r >= 0:
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
    else:
        n_1 = r
        r_1 = n
        r_1 = min(r_1, n_1 - r_1)
        numer = reduce(op.mul, range(n_1, n_1 - r_1, -1), 1)
        denom = reduce(op.mul, range(1, r_1 + 1), 1)
    return numer // denom


def compute_prob_matching_p1(row):
    den = compute_combs(row['Matched_in_P1'], row['Listed_P1'])
    num = compute_combs(row['Matched_in_P1'] - 1, row['Listed_P1'] - 1)
    return num/den


def compute_prob_matching_p2(row):
    den = compute_combs(row['Matched_in_p2'], row['supply_period_2'])
    num = compute_combs(row['Matched_in_p2'] - 1, row['supply_period_2'] - 1)
    return num / den


matching_prob_data = pd.read_pickle(path+'matching_prob_dataset_24')
matching_prob_data['supply_period_2'] = matching_prob_data['Listed_P2'] + matching_prob_data['Listed_P1'] \
                                        - matching_prob_data['Matched_in_P1']

"""matching_prob_data['q_g_1'] = matching_prob_data.apply(compute_prob_matching_p1, axis=1)
matching_prob_data['q_g_2'] = matching_prob_data.apply(compute_prob_matching_p2, axis=1)
"""
matching_prob_data['q_g_1'] = matching_prob_data['Matched_in_P1']/matching_prob_data['Listed_P1']
matching_prob_data['q_g_2'] = matching_prob_data['Matched_in_p2']/matching_prob_data['supply_period_2']

plt.scatter(matching_prob_data['Listed_P1'], matching_prob_data['Matched_in_P1'], label='period_1')
plt.scatter(matching_prob_data['supply_period_2'], matching_prob_data['Matched_in_p2'], label='period_2')
plt.xlabel('Supply')
plt.ylabel('Supply matched')
plt.legend()
plt.show()

plt.scatter(matching_prob_data['Listed_P1'], matching_prob_data['q_g_1'], label='period_1')
plt.scatter(matching_prob_data['supply_period_2'], matching_prob_data['q_g_2'], label='period_2')
plt.xlabel('Supply')
plt.ylabel('Matching_prob')
plt.legend()
plt.show()

plt.scatter(matching_prob_data['Demand_P1'], matching_prob_data['Matched_in_P1'], label='period_1')
plt.scatter(matching_prob_data['Demand_P2'], matching_prob_data['Matched_in_p2'], label='period_2')
plt.legend()
plt.xlabel('demand')
plt.ylabel('Supply matched')
plt.show()

plt.scatter(matching_prob_data['Demand_P1'], matching_prob_data['q_g_1'], label='period_1')
plt.scatter(matching_prob_data['Demand_P2'], matching_prob_data['q_g_2'], label='period_2')
plt.legend()
plt.xlabel('demand')
plt.ylabel('Matching_prob')
plt.show()

# Creating figyre
fig = plt.figure(figsize=(10,6))
ax = axes3d.Axes3D(fig)
ax.scatter3D(matching_prob_data['Demand_P2'], matching_prob_data['supply_period_2'],
             matching_prob_data['Matched_in_p2'], c='r')
ax.set_xlabel('demand')
ax.set_ylabel('supply')
ax.set_zlabel('Supply matched')
plt.show()

fig = plt.figure(figsize=(10,6))
ax = axes3d.Axes3D(fig)
ax.scatter3D(matching_prob_data['Demand_P2'], matching_prob_data['supply_period_2'],
             matching_prob_data['q_g_2'], c='r')
ax.set_xlabel('demand')
ax.set_ylabel('supply')
ax.set_zlabel('Matching_prob')
plt.show()


x_grid = np.linspace(min(matching_prob_data['Demand_P2']), max(matching_prob_data['Demand_P2']), 1000)
y_grid = np.linspace(min(matching_prob_data['supply_period_2']), max(matching_prob_data['supply_period_2']), 1000)
B1, B2 = np.meshgrid(x_grid, y_grid, indexing='xy')
#Z1 = np.zeros((matching_prob_data.size, matching_prob_data.size))
#Z2 = np.zeros((matching_prob_data.size, matching_prob_data.size))

import scipy as sp
import scipy.interpolate
spline = sp.interpolate.Rbf(matching_prob_data['Demand_P2'], matching_prob_data['supply_period_2'],
             matching_prob_data['Matched_in_p2'], function='multiquadric', smooth=20, episilon=1)

Z1 = spline(B1, B2)
fig = plt.figure(figsize=(10, 6))
ax = axes3d.Axes3D(fig)
ax.plot_wireframe(B1, B2, Z1)
ax.plot_surface(B1, B2, Z1, alpha=0.2)
ax.scatter3D(matching_prob_data['Demand_P2'], matching_prob_data['supply_period_2'],
             matching_prob_data['Matched_in_p2'], c='r')
ax.set_xlabel('demand')
ax.set_ylabel('supply')
ax.set_zlabel('Supply matched')
plt.show()

spline = sp.interpolate.Rbf(matching_prob_data['Demand_P2'], matching_prob_data['supply_period_2'],
             matching_prob_data['q_g_2'], function='multiquadric', smooth=20, episilon=1)

Z2 = spline(B1, B2)
fig = plt.figure(figsize=(10, 6))
ax = axes3d.Axes3D(fig)
ax.plot_wireframe(B1, B2, Z2)
ax.plot_surface(B1, B2, Z2, alpha=0.2)
ax.scatter3D(matching_prob_data['Demand_P2'], matching_prob_data['supply_period_2'],
             matching_prob_data['q_g_2'], c='r')
ax.set_xlabel('demand')
ax.set_ylabel('supply')
ax.set_zlabel('Matching_prob')
plt.show()

def early_and_JIT_booking_supply(data, JIT_hours, start_date, end_date):
    time_horizon_list = pd.date_range(start_date, end_date).to_pydatetime()
    early_listers, JIT_listers, JIT_list_percentage, early_list_percentage = [], [], [], []
    early_bookings, JIT_bookings, average_rev_early_listings, average_rev_jit_listing = [], [], [], []
    for i in time_horizon_list:
        df = data[(data.listing_starts <= i) &
                  (data.listing_ends >= i) & (data.listing_length <= 400)][['zap_id', 'id_listing',
                                                                            'listing_starts', 'listing_ends',
                                                                            'listing_created_at']].drop_duplicates()
        df_booking = data[(data.booking_starts <= i) & (data.booking_ends >= i)]
        if df.shape[0] > 0:
            x = df[(i - df.listing_created_at).dt.total_seconds() / 3600 > JIT_hours]
            x_booking = df_booking[(i - df_booking.booking_created_date).dt.total_seconds() / 3600 > JIT_hours]
            early_bookings.append(x_booking.shape[0])
            JIT_bookings.append(df_booking.shape[0] - x_booking.shape[0])
            early_listers.append(x.shape[0])
            JIT_listers.append(df.shape[0] - x.shape[0])
            early_list_percentage.append(x.shape[0] / df.shape[0])
            JIT_list_percentage.append(1 - x.shape[0] / df.shape[0])
            average_rev_early_listings.append(x_booking['booking_fee'].sum() / x.shape[0])
            if df.shape[0] - x.shape[0] > 0:
                average_rev_jit_listing.append((df_booking['booking_fee'].sum() -
                                                x_booking['booking_fee'].sum()) / (df.shape[0] - x.shape[0]))
            else:
                average_rev_jit_listing.append(0)

    # early_listers = df[df.listing_lead_time > 48].shape[0]
    # JIT_listers = df.shape[0] - early_listers

    plt.plot(early_listers, label='suppliers listing early')
    plt.plot(JIT_listers, label='suppliers listing JIT')
    plt.plot(early_bookings, label='early demand')
    plt.plot(JIT_bookings, label='JIT demand')
    plt.show()

    plt.plot(early_list_percentage, label='suppliers listing early')
    plt.plot(JIT_list_percentage, label='suppliers listing JIT')
    plt.legend()
    plt.show()

    plt.plot(average_rev_early_listings, label='ave rev early listing')
    plt.plot(average_rev_jit_listing, label='late_listing_rev')
    plt.legend()
    plt.show()