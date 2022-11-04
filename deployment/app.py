
#!/usr/bin/env python

from flask import Flask,json, render_template,request
import joblib
import pandas as pd


import os

#create instance of Flask app
app = Flask(__name__)

def get_price(user_dict):
    
    my_dict = user_dict.copy()
    user_dict.pop("Type")
    user_ip = pd.DataFrame.from_dict([user_dict])
    if my_dict['Type'] == 'HOUSE':
        predicted_price =joblib.load('model/house_pipeline.pkl').predict(user_ip)
    else:
        predicted_price =joblib.load('model/apartment_pipeline.pkl').predict(user_ip)
    print('predicted price of  user property: ', predicted_price)
    return int(predicted_price)


#decorator 
@app.route("/")
def hello():
    # include information on how to use your API on the home route
    text = '''/form  -------> to input characterstics of your property <br>
              /predict -----> to get prediction of the price '''
              
     
    return render_template('index.html', html_page_text=text)
            
    
@app.route('/form')
def form():
    return render_template('form.html')
    
@app.route("/predict",methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        data_format = {"SubType": "TOWN_HOUSE",
        "NetHabitableSurface(msq)": 211,
        "BedroomCount": "43", 
        "Province": "Limburg",
        "Region": "Flanders",
        "PostCode": "9000", 
       "FacadeCount": "6",
       "KitchenType": "0",
       "Status": "0"
    }    
  
        return render_template('index.html', html_page_text=data_format)
  
    if request.method == 'POST':
        form_data = request.form
        
        property =dict(form_data)
        for key, value in property.items():
            try:
                property[key] = int(value)
            except ValueError:
                property[key] =value
        print(property)
        price = get_price(property)

        response_data = {
        "predicted price": price,
        "status_code": 200
    }
    
        return render_template('index.html',html_page_text =response_data)
            
if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0',port = 5000)
