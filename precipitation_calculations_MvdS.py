# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 12:38:03 2018

@author: Marnix van de Sande
"""

import json

with open('precipitation.json') as file:
    precipitation_data = json.load(file)

seattle_code = "GHCND:US1WAKG0038"
seattle_data = []
for item in range(len(precipitation_data)):
    if precipitation_data[item]['station'] == seattle_code:
        seattle_data.append(precipitation_data[item])

