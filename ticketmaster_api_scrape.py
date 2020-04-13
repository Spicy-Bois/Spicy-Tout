'''
Script takes Ticketmaster API (specifically the events API here) and scrapes initial data for the model, 
exporting to a JSON file in the Data folder.
'''

# Import Libraries
import json
import time
import os
from pathlib import Path

import pandas as pd 
from dotenv import load_dotenv

from ticket_data import Ticket_Data
from tm_api import TM_API

load_dotenv()

# API portal URL
events_api = TM_API('https://app.ticketmaster.com/discovery/v2/events.json?&apikey=',os.getenv('TM_API_KEY'))

# API Query Parameters
parameters = {
    "locale":'en',
    "city" : 'london',
    "page" : '0',
    "size" : '200' # Number of results per page
}

# Define data dictionary
data = Ticket_Data()

# Check whether file is empty
if os.stat(Path('./Data/tm_db.json')).st_size != 0:
    data.add_data(Path('./Data/tm_db.json'))

# Get request
response = events_api.get_response(parameters)

# Loop across TM pages - Currently uses if statements for error handling
# TODO: include proper error handling
page_num = 0
while True:
    
    # Check for valid output in response
    if '_embedded' in response.json(): 

        # Specify part of response corresponding to the event
        tm_events = response.json()["_embedded"].get('events')

        # Loop over events and store in data dictionary
        for event in range(0,len(tm_events)):

            # Event name
            data.data['event'].append(tm_events[event]['name'])
            data.data['date'].append(tm_events[event]['dates']['start']['localDate'])
            
            # Event country
            if 'venues' in tm_events[event]['_embedded'] and 'country' in tm_events[event]['_embedded']['venues'][0] and 'name' in tm_events[event]['_embedded']['venues'][0]['country']:
                data.data['country'].append(tm_events[event]['_embedded']['venues'][0]['country']['name']) 
            else:
                data.data['country'].append('N/A')

            # Event city
            if 'venues' in tm_events[event]['_embedded'] and 'city' in tm_events[event]['_embedded']['venues'][0] and 'name' in tm_events[event]['_embedded']['venues'][0]['city']:
                data.data['city'].append(tm_events[event]['_embedded']['venues'][0]['city']['name']) 
            else:
                data.data['city'].append('N/A')

            # Min price of ticket
            if 'priceRanges' in tm_events[event]:
                data.data['price (min)'].append(tm_events[event]['priceRanges'][0]['min']) 
            else:
                data.data['price (min)'].append('N/A')

            # Max price of ticket
            if 'priceRanges' in tm_events[event]:
                data.data['price (max)'].append(tm_events[event]['priceRanges'][0]['max']) 
            else:
                data.data['price (max)'].append('N/A')

            # Event Venue
            if 'venues' in tm_events[event]['_embedded'] and 'name' in tm_events[event]['_embedded']['venues'][0]:
                data.data['venue'].append(tm_events[event]['_embedded']['venues'][0]['name']) # Venue
            else:
                data.data['venue'].append('N/A')
            
            # Event Genre
            if 'classifications' in tm_events[event] and 'genre' in tm_events[event]['classifications'][0] and 'name' in tm_events[event]['classifications'][0]['genre']:
                data.data['genre'].append(tm_events[event]['classifications'][0]['genre']['name']) # Venue
            else:
                data.data['genre'].append('N/A')

    else:
        break

    # Itterate through pages and update API response
    page_num += 1
    # Pause loop
    if page_num % 5 == 0:
        time.sleep(1)
    response = events_api.change_page(page_num)

# Create DataFrame 
df = pd.DataFrame(data.data)

# Remove duplicates
df.drop_duplicates(keep='first',inplace=True) 

# TODO: Error handling, again
# Export data to .json file 
df.to_json(Path('./data/tm_db.json'),orient='records')