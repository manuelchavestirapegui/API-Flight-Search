import requests
from pprint import pprint

SHEETY_ENDPOINT = 'https://api.sheety.co/d5a238b4aa2fd759785a45132ddc489b/flightDeals/prices'


class DataManager:
    def __init__(self):
        self.destination_data = {}

    # Save as destination_data a list of dictionaries with the data contained in the excel
    def get_destination_data(self):
        response = requests.get(SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data['prices']
        pprint(self.destination_data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(f'{SHEETY_ENDPOINT}/{city["id"]}', json=new_data)
            print(response.text)

    def update_cheapest_price(self, cheapest_prices_data):
        for city in cheapest_prices_data:
            new_data = {
                'price': {
                    'lowestPrice': city['lowestPrice']
                }
            }
            response = requests.put(f'{SHEETY_ENDPOINT}/{city}', json=new_data)
            print(response.text)
