# real-estate-price-prediction
## Description

This project is a use case given by a real estate company in Belgium. Two prediction models are created to predict the price of real estate sales in Belgium. First, raw data is scraped from the web. And then is cleaned and further processed to train a model. Finally, the model is deployed with a flask.

## Installation
To deploy and use the project first clone it and use the deployment

### method 1:  using a virtual environment

1. Install a virtual environment

```
pip install virtualenv
```
2. Create a virtual environment and activate it
```
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . env/bin/activate
```
3. Install the list of libraries in the requirements.txt
```
pip install -r requirements.txt
```
4. run the app.py file
```
python app.py

```
And go to the link http://127.0.0.1:5000 from the resulting terminal

### method 2: Using Docker

 First, install docker in your machine and go to the deployment directory on your terminal and type the following commands
```
docker build . -t property_predict
docker run -p 5000:5000 property_predict

```
The above command will create and run an image for the project.




user has to put their property(house/apartment) characterstics in the form and 
and the model will predict the price of the property:


assets/user_form.png
assets/output_data.png
![user form ](assets/user_form.png)
![output ](assets/output_data.png)



## Contributors

Amanuel Zeredawit
@ becode, Gent 2022










