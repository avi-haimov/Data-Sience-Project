from bs4 import BeautifulSoup
import os 
from os.path import isfile, join
import pandas as pd 
import re
import numpy as np


def set_arrays_the_same_length(array1,array2):
    while len(array2) < len(array1):
        array2.append(np.nan)
    
    return array2

mypath = os.path.abspath(__file__).replace('test.py','')
dir_list = os.listdir("C:\\Users\\almog\\Desktop\\Project\\data\\TenBis\\")
total_ranking = []
total_times = []
total_rankers = []
total_delivery_fee = []
total_names = []
total_min_order = []
total_countries = []
currency_converter = {
    "Ireland" : 1,
    "New Zeland": 0.6,
    "Australia" : 0.66,
    "England": 1.17
    }

print("The project takes a time to load.. 5~ minutes.. \n")
print("Thank you for your patience...\n")
for folder in dir_list:
    file_list = os.listdir("C:\\Users\\almog\\Desktop\\Project\\data\\TenBis\\" + folder)
    for file in file_list:
        soup = BeautifulSoup(open("C:\\Users\\almog\\Desktop\\Project\\data\\TenBis\\" + folder + "\\" + file,encoding = "utf8"),"html.parser")
        #names
        divs_names = soup.find_all("h3", attrs = {"class":"RestaurantCard_c-restaurantCard-name_1Zwfd"})
        names = [name.get_text() for name in divs_names]
        total_names.extend(names)
        #ranking
        divs_ranking = soup.find_all("data", attrs = {"class":"RestaurantRating_c-restaurantCard-rating-mean_2nucs"})
        ranking = [rank.get_text() for rank in divs_ranking]
        total_ranking.extend(ranking)
        #Amount of rankers
        divs_rankers = soup.find_all("data", attrs = {"class":"RestaurantRating_c-restaurantCard-rating-count_1HT6D"})
        rankers = [ranker.get_text() for ranker in divs_rankers]
        total_rankers.extend(rankers)
        #Country
        for i in range(len(names)):
            total_countries.append(folder)
        #time, min order, delivery fee
        divs = soup.find_all("span", attrs = {"class":"IconText_c-restaurantCard-iconText-content_2wOUu"})
        for anomaly in divs:
            if "mins" in anomaly.get_text():
                total_times.append(anomaly.get_text()[5:8])
            elif "Delivery" in anomaly.get_text():
                if "FREE" in anomaly.get_text():
                    total_delivery_fee.append(0)
                else:
                    if len(anomaly.get_text()) == 14:
                        if "from" in anomaly.get_text():
                            total_delivery_fee.append(float(anomaly.get_text()[10:]) * currency_converter[folder])
                        else:
                            total_delivery_fee.append(float(anomaly.get_text()[11:13]) * currency_converter[folder])
                    elif len(anomaly.get_text()) == 19:
                        total_delivery_fee.append(float(anomaly.get_text()[15:])* currency_converter[folder])
                    elif len(anomaly.get_text()) == 16:
                        total_delivery_fee.append(float(anomaly.get_text()[11:15])* currency_converter[folder])
                    elif len(anomaly.get_text()) == 21:
                        total_delivery_fee.append(float(anomaly.get_text()[16:20])* currency_converter[folder])
                    else:
                        total_delivery_fee.append('')
            elif "min." in anomaly.get_text() or "Min." in anomaly.get_text():
                if "No" in anomaly.get_text():
                    total_min_order.append(0)
                elif len(anomaly.get_text()) > 13:
                    #try:
                        total_min_order.append(float(anomaly.get_text()[13:])* currency_converter[folder])
                    #except:
                        #print(anomaly.get_text())     
                else:
                    total_min_order.append('')
        total_ranking = set_arrays_the_same_length(total_names,total_ranking)
        total_times = set_arrays_the_same_length(total_names,total_times)
        total_rankers = set_arrays_the_same_length(total_names,total_rankers)
        total_delivery_fee = set_arrays_the_same_length(total_names,total_delivery_fee)
        total_min_order = set_arrays_the_same_length(total_names,total_min_order)
        total_countries = set_arrays_the_same_length(total_names,total_countries)
df = pd.DataFrame({"names":total_names,"countries":total_countries,"min_order":total_min_order,"delivery_fee":total_delivery_fee,"amount_of_rankers":total_rankers,"delivery_time_MAX":total_times,"ranking":total_ranking})
df.to_csv("C:\\Users\\almog\\Desktop\\Project\\DataFrame.csv")
print("Done!\n")     
                    
                
#tasks
#create and save the df as csv
#start working on the next stage of the project (creating the ML model and the rest of what is in the presentation)                
#check if it's possible to do an api call to the google drive folder to get the html files

