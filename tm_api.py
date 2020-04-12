import requests
'''Class specifically for TM APIs'''

class TM_API:

    # Use API url up to 'APIkey='
    def __init__(self, api_url, TM_API_KEY):
        
        self.endpoint = api_url + TM_API_KEY
    
    def get_response(self,parameters={}):

        self.parameters = parameters
        return (requests.get(self.endpoint, params=self.parameters))

    def change_page(self, page_num = '0'):

        if 'page' in self.parameters:
            self.parameters['page'] = str(page_num)
        else:
            self.parameters.update({'page':str(page_num)})

        return self.get_response(self.parameters)
        