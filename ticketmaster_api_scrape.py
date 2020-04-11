# Import Libraries
import requests
import json
import time
import pandas as pd 
import os

from dotenv import load_dotenv
from pathlib import Path

from ticket_data import Ticket_Data

load_dotenv()

# API portal URL
TM_KEY = os.getenv('TM_API_KEY')
api_url = f'https://app.ticketmaster.com/discovery/v2/events.json?&apikey={TM_KEY}'

# API Query Parameters
parameters = {
    "locale":'en',
    "city" : 'london',
    "page" : '0',
    "size" : '2' # Number of results per page
}

# Define data dictionary
data = Ticket_Data()
# data.add_data(Path('./Data/tm_db.json'))

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

    page_num += 1

    if page_num > 1:
        break

    # Pause loop
    if page_num % 5 == 0:
        time.sleep(1)



# TODO: Logic to remove duplicates

# Create DataFrame 
df = pd.DataFrame(data.data)
  
# TODO: Error handling, again
# Export data to .json file 
df.to_json(Path('./data/tm_db.json'),orient='records')