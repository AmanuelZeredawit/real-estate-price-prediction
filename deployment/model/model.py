import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

def cleaning_data():
    df = pd.read_csv(r"C:\Users\32467\OneDrive\Documents\Arai4_Projects\real-estate-price-prediction\assets\data.csv")
    city = df['PostCode'].apply(lambda x: str(x)[0:2])
    df['City']= city
    age = df['ConstructionYear'].apply(lambda x: 2022-x)
    df['Age'] = age
    df = df.drop(['BuildingCondition','ConstructionYear','RegionCode','Locality','ID','Age','City','Floor','HasBalcony','HasGarden'], axis =1)
    grouped_df = df.groupby(df.Type)
    return grouped_df



def get_data(type,grouped_df):
    
    if type == 'house':
        df_house = grouped_df.get_group("HOUSE").drop(['Type'],axis =1)
        y= df_house['Price'].copy().to_numpy()
        X = df_house.drop('Price', axis=1)
    else:
        df_apartment = grouped_df.get_group("APARTMENT").drop(['Type'],axis =1)
        y = df_apartment['Price'].copy().to_numpy()
        X = df_apartment.drop('Price', axis=1)
      # split the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=1/5,random_state=0)  
    return X_train, X_test, y_train, y_test



def my_pipeline():
    num_attribs = ['NetHabitableSurface(msq)','BedroomCount']
    cat_attribs = ['Region','Province','SubType','KitchenType','FacadeCount','PostCode']

    num_tr_pipeline = Pipeline([
        ('std_scaler', StandardScaler()),])
    
    cat_tr_pipeline = Pipeline([
        ('one_hot_encoder', OneHotEncoder(sparse=False, handle_unknown='ignore')),])
    preprocessors = ColumnTransformer([
        ("num_tr_pipeline", num_tr_pipeline, num_attribs),
        ("cat_tr_pipeline", cat_tr_pipeline, cat_attribs),])
    
    pipe =Pipeline([
    ('prepocessors',preprocessors),
    ('random_forest',RandomForestRegressor(n_estimators=200, random_state=0)),])
    
    return pipe

def get_model():
    grouped_df = cleaning_data()
    # get model for house
    X_train, X_test, y_train, y_test = get_data('house',grouped_df)
    pipe = my_pipeline()
    pipe.fit(X_train,y_train)
    joblib.dump(pipe, 'house_pipeline.pkl')
    y_pred = pipe.predict(X_test)
    print('score for house model :',pipe.score(X_test,y_test))

    # get model for apartment
    X_train, X_test, y_train, y_test = get_data('apartment',grouped_df)
    pipe.fit(X_train,y_train)
    joblib.dump(pipe, 'apartment_pipeline.pkl')
    y_pred = pipe.predict(X_test)
    print('score for apartment model :',pipe.score(X_test,y_test))

def predict_price():
    user_dict= {'Type':'HOUSE','SubType':'HOUSE', 'NetHabitableSurface(msq)':200, 'BedroomCount':2,
       'Province':'Antwerpen', 'Region':'Flanders', 'PostCode':9000, 'FacadeCount':3, 'KitchenType':'1',
       'Status': 'old'}
    my_dict = user_dict.copy()
    user_dict.pop("Type")
    user_ip = pd.DataFrame.from_dict([user_dict])
    if my_dict['Type'] == 'HOUSE':
        predicted_price =joblib.load('house_pipeline.pkl').predict(user_ip)
    else:
        predicted_price =joblib.load('apartment_pipeline.pkl').predict(user_ip)
    print('predicted price of  user property: ', predicted_price)

get_model()
predict_price()
