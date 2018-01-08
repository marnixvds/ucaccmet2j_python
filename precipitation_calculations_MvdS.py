# -*- coding: utf-8 -*-
import json

#Load JSON file into a list of dictionaries
with open('precipitation.json') as file:
    precipitation_data = json.load(file)

#Make a dictionary with stations from CSV file
with open('stations.csv') as file:
    stations = {}
    headers = file.readline()
    for line in file:
        (Location, State, Station) = line.strip().split(',')
        stations[Location] = {'State' : State, 'Station' : Station}

result_dictionary = {} #Create a dict for final results
#Calculate the yearly precipitation in the entire country --> Values are added in the most nested loop, to make sure everything is included.
total_country_precipitation = 0

#Create a loop to go over all the weather stations
for chosen_station in stations.keys():
    #Define weather station code of interest and create an empty list for the filtered data
    state = stations[chosen_station]['State'] #State code
    station_code = stations[chosen_station]['Station'] #Station code
    station_data = [] #Empty list to add station data
    
    #Filter out all the entries for the station of interest, and add them to the newly created list
    for item in range(len(precipitation_data)):
        if precipitation_data[item]['station'] == station_code:
            station_data.append(precipitation_data[item])
    
    #Organise data per month
    precipitation_per_month = [] #New data list for all the months [Jan, Feb, Mar...]
    for month in range(1, 13): #Loop over the 12 months, sum up all values for that month
        month_data = 0
        for measurement in range(len(station_data)): # Check for all entries whether they correspond to the 'current' month
            if '2010-'+str(month).zfill(2) in station_data[measurement]['date']:
                month_data += station_data[measurement]['value'] #Sum up all the values for this month
                total_country_precipitation += station_data[measurement]['value'] #Also add the value to the total country rain count
        precipitation_per_month.append(month_data) #Add the sum for this month to the month list.
    
    #Calculate sum of precipitation for the whole year for this station
    precipitation_whole_year = sum(precipitation_per_month)
    #Calculate relative precipitation (% compared to whole year)
    relative_monthly_precipitation =[]
    for month in range(0, 12):
        relative_monthly_precipitation.append((precipitation_per_month[month]/precipitation_whole_year)*100)
    
    #Calculate the relative precipitation of this state
    relative_state_precipitation = (precipitation_whole_year/total_country_precipitation)*100
    
    #Add all the results the final dictionary
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