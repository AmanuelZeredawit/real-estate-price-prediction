FROM python:3.10
#WORKDIR /deployment
EXPOSE 5000
# Install app dependecy 
RUN mkdir /deployment
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /deployment
CMD [ "python3", "deployment/app.py"]