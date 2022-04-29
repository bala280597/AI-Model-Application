import pandas as pd
import os
import gcsfs
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../auth.json'

def load_joblib(bucket_name, file_name):
    fs = gcsfs.GCSFileSystem()
    with fs.open(f'{bucket_name}/{file_name}') as f:
        return pd.read_csv(f)
df = load_joblib('aiml-dataset', 'USA_Housing.csv')
x = df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
       'Avg. Area Number of Bedrooms', 'Area Population']]
y = df['Price']
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.4,random_state=101)
lm = LinearRegression()
lm = lm.fit(X_train, y_train)
joblib.dump(lm,"house.pkl")
