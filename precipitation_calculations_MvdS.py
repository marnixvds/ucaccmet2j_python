# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 12:38:03 2018

@author: Marnix van de Sande
"""

import json

#Load JSON file into a list of dictionaries
with open('precipitation.json') as file:
    precipitation_data = json.load(file)

#Make a dictionary out of the stations CSV file
with open('stations.csv') as file:
    stations = {}
    headers = file.readline()
    for line in file:
        (Location, State, Station) = line.strip().split(',')
        stations[Location] = {
                'State' : State,
                'Station' : Station
                }

#Calculate the yearly precipitation in the entire country --> For % state. I now used a loop, but is there a way to sum() this?
total_country_precipitation = 0
for item in range(len(precipitation_data)):
    total_country_precipitation += precipitation_data[item]['value']
    
result_dictionary = {}
for chosen_station in stations.keys():
    #Define weather station code of interest and create an empty list for the filtered data
    state = stations[chosen_station]['State']
    station_code = stations[chosen_station]['Station']
    station_data = []
    
    #Filter out all the entries for the station of interest, and add them to the newly created list
    for item in range(len(precipitation_data)):
        if precipitation_data[item]['station'] == station_code:
            station_data.append(precipitation_data[item])
    
    #Organise data per month
    precipitation_per_month = [] #New final data list [Jan, Feb, Mar...]
    for month in range(1, 13): #Loop over the 12 months, sum up all values for that month
        tmp_data = []
        for measurement in range(len(station_data)): # Check for all entries whether they correspond to the 'current' month
            if '2010-'+str(month).zfill(2) in station_data[measurement]['date']:
                tmp_data.append(station_data[measurement]['value']) #Add all the values for this month to a temporary list
        precipitation_per_month.append(sum(tmp_data)) #Add the sum of this temporary list (all the measurements for one month) to the final data.
    
    #Calculate sum of prep for the whole year
    precipitation_whole_year = sum(precipitation_per_month)
    #Calculate relative precipitation (% compared to whole year)
    relative_monthly_precipitation =[]
    for month in range(0, 12):
        relative_monthly_precipitation.append((precipitation_per_month[month]/precipitation_whole_year)*100)
    
    #Calculate the relative precipitation of this state
    relative_state_precipitation = (precipitation_whole_year/total_country_precipitation)*100
    
    #Put all the results together into one dictionary
    result_dictionary[chosen_station] = {
            'station': station_code,
            'state': state,
            'totalMonthlyPrecipitation': precipitation_per_month,
            'relativeMonthlyPrecipitation': relative_monthly_precipitation,
            'totalYearlyPrecipitation': precipitation_whole_year,
            'relativeYearlyPrecipitation': relative_state_precipitation            
            }

with open('result.json', 'w') as file: #Export the final data to a JSON file
    json.dump(result_dictionary, file, indent=4)