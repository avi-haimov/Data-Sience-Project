from bs4 import BeautifulSoup
import os 
from os.path import isfile, join
import pandas as pd 
import re


     

mypath = ".\\data"
dir_list = os.listdir(".\\data\\TenBis")
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
for folder in dir_list:
    file_list = os.listdir(".\\data\\TenBis\\" + folder)
    for file in file_list:
        soup = BeautifulSoup(open(".\\data\\TenBis\\" + folder + "\\" + file,encoding = "utf8"),"html.parser")
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
                total_times.append(anomaly.get_text()[5:7])
            elif "Delivery" in anomaly.get_text():
                if "FREE" in anomaly.get_text():
                    total_delivery_fee.append(0)
                else:
                    if len(anomaly.get_text()) == 14:
                        total_delivery_fee.append(float(anomaly.get_text()[11:]) * currency_converter[folder])
                    elif len(anomaly.get_text()) == 19:
                        total_delivery_fee.append(float(anomaly.get_text()[15:])* currency_converter[folder])
                    else:
                        total_delivery_fee.append('')
            elif "min." in anomaly.get_text() or "Min." in anomaly.get_text():
                if "No" in anomaly.get_text():
                    total_min_order.append(0)
                elif len(anomaly.get_text()) > 13:
                    #try:
                        total_min_order.append(float(anomaly.get_text()[13:]))
                    #except:
                        #print(anomaly.get_text())     
                else:
                    total_min_order.append('')
df = pd.DataFrame({"names":total_names,"countries":total_countries,"min_order":total_min_order,"delivery_fee":total_delivery_fee,"amount_of_rankers":total_rankers,"delivery_time_MAX":total_times,"ranking":total_ranking})
print("Done")           
                    
                
                
    
    

#check if it's possible to do an api call to the google drive folder to get the html files

