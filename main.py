from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_CODE = 'VLC'

#Update the code with the information found in get_destination_codes in flight_search
if sheet_data[0]['iataCode'] == '':
    for row in sheet_data:
        row['iataCode'] = flight_search.get_destination_code(row['city'])
    pprint(f'sheet_data:\n {sheet_data}')

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

#Set days from now to 6 months ahead to look for flight in that range
now = datetime.now() + timedelta(days=1)
tomorrow = now.strftime('%d/%m/%Y')
in_six_months = now + timedelta(days=180)
flight_to = in_six_months.strftime('%d/%m/%Y')

destination_codes = []
for destination in sheet_data:
    destination_codes.append(destination['iataCode'])
print(f'sheet_data:\n {sheet_data}')

#Send the notification if there are new cheapest flights for each destination and update the new values.
for destination in sheet_data:
    flight = flight_search.find_cheap_flights(
        origin_code=ORIGIN_CITY_CODE,
        destination_codes=destination['iataCode'],
        from_time=tomorrow,
        to_time=flight_to
    )
    if flight is None:
        continue
    if flight.price < destination['lowestPrice']:
        notification_manager.send_email(
            message=f'Subject:Cheap Flight Alert!\n\n '
                    f'There is a flight '
                    f'from {flight.origin_city}-{flight.origin_airport} '
                    f'to {flight.destination_city}-{flight.destination_airport} '
                    f'from {flight.out_date} '
                    f'to {flight.return_date} '
                    f'for only {flight.price} euros')
        data_manager.update_cheapest_price(flight_search.cheapest_prices_dict)

