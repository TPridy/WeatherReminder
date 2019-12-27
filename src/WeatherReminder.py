#############################################################################################
# File name: WeatherReminder.py    								    			            #				        
#																							#			  
# Created by Thomas Pridy on 12/27/19														#  
# Copyright  2019 Thomas Pridy. All rights reserved.							            #																			#	  
#     																						#		  
#############################################################################################
import json
from threading import Timer
from datetime import datetime, timedelta
from twilio.rest import Client
import requests

#############################################################################################
# Initialization                                                                            #
#############################################################################################
#Twilio Authentication
account_sid = 'AC0b1a68e0aad45414ee76c0fab0c5b548'
auth_token = '90c7ddad7c476811c8460679424bd49b'
client = Client(account_sid, auth_token)

#Timer and Weather Settings
HOUR = 7
MINUTE = 0
SECOND = 0 
LATITUDE = 33.7701
LONGITUDE = -118.1937

#############################################################################################
# Main Definition                                                                           #
#############################################################################################
def main():  
    configureTimer()

#############################################################################################
# Fucntion Definitions                                                                      #
#############################################################################################

#-------------------------------------------------------------------------------------------#
# send_message() uses the Twilio API to send a text message of the current weather data     #
# using a call to a user defined function getWeather(). It then calls configureTimer()      #
# to reconfigure the timer for the same time on the following day                           #
#-------------------------------------------------------------------------------------------#
def send_message(): 
    message = client.messages \
                .create(
                     body= getWeather(),
                     from_='+17142480061',
                     to='+15622094643'
                )
    print(message.sid)
    configureTimer()

#-------------------------------------------------------------------------------------------#
# configureTimer() starts a timer thread for the values stored in the variables:            #
# HOUR,  MINUTE, and SECOND. Once the timer thread has reached the set time, it calls the   # 
# function send_message()                                                                   #
#-------------------------------------------------------------------------------------------#
def configureTimer():
    x=datetime.today()
    y = x.replace(day=x.day, hour=HOUR, minute=MINUTE, \
                  second=SECOND, microsecond=0) + timedelta(days=1)
    delta_t=y-x
    secs=delta_t.total_seconds()
    t = Timer(secs, send_message)
    t.start()

#-------------------------------------------------------------------------------------------#
# getWeather() uses the weatherbit API to gather the current weather information based on   #
# the latitude and longitude of the valus set it LANGITUDE, LONGITUDE. getWeather() then    #
# augments the response from the API to construct a string and return it.                   #
#-------------------------------------------------------------------------------------------#
def getWeather():
    #WeatherBit  Authentication
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"
    querystring = {"lang":"en","lon":str(LONGITUDE),"lat":str(LATITUDE), "units" : "I"}
    headers = {
        'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
        'x-rapidapi-key': "15fb81d8e0msh5eca1c503c1682cp1b4680jsn0c41a68b877a"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    weather = response.json()

    #Dividing Json response
    city  = weather.get('data')[0].get("city_name")
    state = weather.get('data')[0].get("state_code")
    desc  = weather.get('data')[0].get("weather").get("description")
    temp  = str(weather.get('data')[0].get("temp"))
    precip= str(weather.get('data')[0].get("precip")) 

    #Construction of weather string
    message = "Weather Forecast for " + city + ',' + state + ": \n" \
              "Description: " + desc + "\n" \
              "Temperature: " + temp + "\n" \
              "Precipitation: " + precip + "%"
    
    #Return Statement
    return message
#############################################################################################
# Call to main                                                                              #
#############################################################################################
main()
