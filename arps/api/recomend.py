import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from datetime import datetime
from django.conf import settings
import os

static_dir = settings.STATIC_ROOT

data = pd.read_csv(os.path.join(static_dir ,'Crop_recommendation.csv'))

y = data['label']
x = data.drop(['label'], axis=1)

transformer = ColumnTransformer([('num', StandardScaler(), x.columns)])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)

svm_pipe = Pipeline(steps=[('preprocessing', transformer), ('model', SVC())])

svm_pipe.fit(x_train, y_train)
y_pred = svm_pipe.predict(x_test)

logis_pipe = Pipeline(steps=[("preprocessing", transformer), ("model", LogisticRegression())])
logis_pipe.fit(x_train, y_train)
y_pred = logis_pipe.predict(x_test)

tree_pipe = Pipeline(steps=[("preprocessing", transformer), ("model", DecisionTreeClassifier())])
tree_pipe.fit(x_train, y_train)
y_pred = tree_pipe.predict(x_test)

with open(os.path.join(static_dir ,'prediction_tree_model.pkl'), 'wb') as file:
    pickle.dump(tree_pipe, file)

def getNewData(N, P, K, temperature, humidity, ph, rainfall):
    new_data = {'N': [N], 'P': [P], 'K': [K], 'temperature': [temperature], 'humidity': [humidity], 'ph': [ph], 'rainfall': [rainfall]}
    return new_data

def predictCrop(new_data):
    prediction_proba = tree_pipe.predict_proba(pd.DataFrame(new_data))
    crops = tree_pipe.classes_
    sorted_crops = [x for _, x in sorted(zip(prediction_proba[0], crops), reverse=True)]
    return sorted_crops[:5]


def recomendCrop(N, P, K, ph, location):
    current_month_number = datetime.now().month
    mean_data = pd.read_csv(os.path.join(static_dir ,'mean_data.csv'))
    location_month_data = mean_data[(mean_data['DISTRICT'] == location) & (mean_data['MONTH'] == current_month_number)]
    selected_data = location_month_data[['PRECTOT', 'T2M_MEAN', 'RH2M']]
    temperature = selected_data['T2M_MEAN'].values[0]
    humidity = selected_data['RH2M'].values[0]
    rainfall = selected_data['PRECTOT'].values[0]
    N = float(N)
    P = float(P)
    K = float(K)
    ph = float(ph)
    return predictCrop(getNewData(N, P, K, temperature, humidity, ph, rainfall))