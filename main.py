#import the neccessary libraries for the code
from calendar import EPOCH
from urllib import response
import requests
import boto3
import pandas as pd
import os
import json
from datetime import datetime
from contextlib import redirect_stdout

#this is the url to the API we call to receive our weather data
url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"

#Below we allow the end user to insert a specific city & date range, also set a date_time variable.
#There are some defaults in place if you wanted to just click enter to quickly test the api 
city_name = input("Enter the city name (leave blank to default to Detroit): ") or 'Detroit'
date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
start_date = input("Enter Start Date yyyy-mm-dd: ") or date_time
end_date = input("Enter End Date yyyy-mm-dd: ") or date_time
data_list = []
#set parameters in a dictionary key/value list for the api url this helps get specifc results
#the header stores the host url, our api key and the result file type
querystring = {
            "q": f"{city_name}, {start_date}, {end_date}",
            "cnt": "7",
            "mode": "json",
            "type": "accurate",
            "units": "imperial",
        }

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key' : "1290077c8cmsh89c26c51f18a8e4p1f122cjsn597138fb4300",
    'content-type'   : 'application/json'
    }
#now we call the API to "GET" our weather data and we receice a response/result that is pushed to our S3 bucket
response = requests.request("GET", url, headers=headers, params=querystring)
data_list = []
#Creating S3 Resource From the Client.
content = json.loads(response.text)
data_list.append(pd.DataFrame([content]))
df = pd.json_normalize(data_list)
df
dl = pd.concat(data_list,ignore_index=True, sort=False)
csv_body = dl.to_csv(index=False)
s3 = boto3.client('s3')
s3.put_object(Body=csv_body, Bucket='public-weather-cities', Key=f"cities/{city_name}.csv")
print ("-------------------------------------------------------------")
print ("7 Day Weather Forecast for - {}  || {}".format(city_name.upper(), date_time))
print ("-------------------------------------------------------------")
print ("Weather API Response saved to AWS Bucket - s3://public-weather-cities/cities/ ")