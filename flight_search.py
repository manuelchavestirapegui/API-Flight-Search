import requests
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get("TEQUILA_API_KEY")


class FlightSearch:

    def __init__(self):
        self.headers = {'apikey': TEQUILA_API_KEY}
        self.cheapest_prices_dict = []

    # This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        location_endpoint = f'{TEQUILA_ENDPOINT}/locations/query'
        query = {'term': city_name, 'location_types': 'city'}
        response = requests.get(url=location_endpoint, headers=self.headers, params=query)
        data = response.json()['locations']
        code = data[0]['code']
        return code

    def find_cheap_flights(self, origin_code, destination_codes, from_time, to_time):
        location_endpoint = f'{TEQUILA_ENDPOINT}/v2/search'
        query = {
            'fly_from': origin_code,
            'fly_to': destination_codes,
            'date_from': from_time,
            'date_to': to_time,
            'nights_in_dst_from': 3,
            'nights_in_dst_to': 7,
            'flight_type': 'round',
            'curr': 'EUR',
            'one_for_city': 1,
            'max_stopovers': 0,
        }

        response = requests.get(url=location_endpoint, headers=self.headers, params=query)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_codes}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(
            f"{flight_data.destination_city}: €{flight_data.price}, from: {flight_data.out_date}, to {flight_data.return_date}")
        self.cheapest_prices_dict.append({'lowestPrice': flight_data.price})
        print(self.cheapest_prices_dict)
        return flight_data
