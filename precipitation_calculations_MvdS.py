# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 12:38:03 2018

@author: Marnix van de Sande
"""

import json

#Load JSON file into a list of dictionaries
with open('precipitation.json') as file:
    precipitation_data = json.load(file)

#Define weather station code of interest and create an empty list for the filtered data
seattle_code = "GHCND:US1WAKG0038"
seattle_data = []

#Filter out all the entries for the station of interest, and add them to the newly created list
for item in range(len(precipitation_data)):
    if precipitation_data[item]['station'] == seattle_code:
        seattle_data.append(precipitation_data[item])

#Organise data per month
precipitation_per_month = [] #New final data list [Jan, Feb, Mar...]
for month in range(1, 13): #Loop over the 12 months, sum up all values for that month
    tmp_data = []
    for measurement in range(len(seattle_data)): # Check for all entries whether they correspond to the 'current' month
        if '2010-'+str(month).zfill(2) in seattle_data[measurement]['date']:
            tmp_data.append(seattle_data[measurement]['value']) #Add all the values for this month to a temporary list
    precipitation_per_month.append(sum(tmp_data)) #Add the sum of this temporary list (all the measurements for one month) to the final data.

with open('seattle_data.json', 'w') as file: #Export the final data to a JSON file
    json.dump(precipitation_per_month, file, indent=4)