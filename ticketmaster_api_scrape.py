# Import Libraries
import requests
import json
import time
import pandas as pd 
import os

from dotenv import load_dotenv

load_dotenv()

# API portal URL
TM_KEY = os.getenv('TM_API_KEY')
api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?&apikey={TM_KEY}'

# API Query Parameters
parameters = {
    "locale":'en',
    "city" : 'london',
    "page" : '0',
    "size" : '200' # Number of results per page
}

data = {
    'event' : [],
    'date' : [],
    'country' : [],
    'city' : [],
    'price (min)' : [],
    'price (max)' : [],
    'venue' : [],
    'genre' : []
}

page_num = 0

# Loop across TM pages - Currently uses if statements for error handling
# TODO: include proper error handling

while True:

    # Set page number
    parameters['page'] = str(page_num)
    # Get request
    response = requests.get(api_url, params=parameters)
    
    # Check for valid output in response
    if '_embedded' in response.json(): 

        # Specify part of response corresponding to the event
        tm_events = response.json()["_embedded"].get('events')

        # Loop over events and store in data dictionary
        for event in range(0,len(tm_events)):

            # Event name
            data['event'].append(tm_events[event]['name'])
            data['date'].append(tm_events[event]['dates']['start']['localDate'])
            
            # Event country
            if 'venues' in tm_events[event]['_embedded'] and 'country' in tm_events[event]['_embedded']['venues'][0] and 'name' in tm_events[event]['_embedded']['venues'][0]['country']:
                data['country'].append(tm_events[event]['_embedded']['venues'][0]['country']['name']) 
            else:
                data['country'].append('N/A')

            # Event city
            if 'venues' in tm_events[event]['_embedded'] and 'city' in tm_events[event]['_embedded']['venues'][0] and 'name' in tm_events[event]['_embedded']['venues'][0]['city']:
                data['city'].append(tm_events[event]['_embedded']['venues'][0]['city']['name']) 
            else:
                data['city'].append('N/A')

            # Min price of ticket
            if 'priceRanges' in tm_events[event]:
                data['price (min)'].append(tm_events[event]['priceRanges'][0]['min']) 
            else:
                data['price (min)'].append('N/A')

            # Max price of ticket
            if 'priceRanges' in tm_events[event]:
                data['price (max)'].append(tm_events[event]['priceRanges'][0]['max']) 
            else:
                data['price (max)'].append('N/A')

            # Event Venue
            if 'venues' in tm_events[event]['_embedded'] and 'name' in tm_events[event]['_embedded']['venues'][0]:
                data['venue'].append(tm_events[event]['_embedded']['venues'][0]['name']) # Venue
            else:
                data['venue'].append('N/A')
            
            # Event Genre
            if 'classifications' in tm_events[event] and 'genre' in tm_events[event]['classifications'][0] and 'name' in tm_events[event]['classifications'][0]['genre']:
                data['genre'].append(tm_events[event]['classifications'][0]['genre']['name']) # Venue
            else:
                data['genre'].append('N/A')

            

    else:
        break

    page_num += 1

    # Pause loop
    if page_num % 5 == 0:
        time.sleep(1)

# Create DataFrame 
df = pd.DataFrame(data) 
  
# Print the output. 
# TODO: determine how we want to export dataframe
print(df.head())