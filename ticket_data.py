import json

class Ticket_Data:
    def __init__(self):
        
        self.data = {
                    'event' : [],
                    'date' : [],
                    'country' : [],
                    'city' : [],
                    'price (min)' : [],
                    'price (max)' : [],
                    'venue' : [],
                    'genre' : []
                }

    #TODO: Error handling for wrong/ no file
    def add_data(self, events_file):
        with open(events_file, 'r') as events:
            dict = json.load(events)

        
        for entry in dict:
            for key, value in entry.items():
                self.data[key].append(value)


if __name__ == "__main__":
    pass