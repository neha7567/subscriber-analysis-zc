import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


categories = ['below 30', '30-50', 'greater than 50']


def age_assignment(row):
    if row['Age '] >= 50:
        v = categories[2]
    elif row['Age '] <= 30:
        v = categories[0]
    else:
        v = categories[1]
    return v


path = 'C:\\Users\\Neha Sharma\\Google Drive\\ZoomCar_data\\subscriber_data\\'
subscriber_details_data = pd.read_pickle(path + 'data_subscriber_details')
survey_data = pd.read_csv(path+'zap_user_survey_form.csv').drop(columns=['dt'])
survey_data = survey_data.drop_duplicates()


subscriber_details_data = pd.merge(left=subscriber_details_data, right=survey_data,
                                   left_on='zap_id', right_on='zap_subscription_id')
subscriber_details_data['Age '] = pd.to_numeric(subscriber_details_data['Age '], errors='coerce')
subscriber_details_data['age_category'] = subscriber_details_data.apply(age_assignment, axis=1)


sns.scatterplot(x='mean_subscription_fee', y='mean_earnings', hue='age_category', data= subscriber_details_data)
plt.show()
