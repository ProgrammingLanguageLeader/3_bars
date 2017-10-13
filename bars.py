import json
import os
import urllib.request
from math import asin
from math import sin
from math import cos
from math import sqrt
from math import radians


def get_bars_features(bar_data):
    return bar_data['features']


def get_bar_attributes(feature):
    return feature['properties']['Attributes']


def get_bar_seats_count(feature):
    return get_bar_attributes(feature)['SeatsCount']


def get_bar_name(feature):
    return get_bar_attributes(feature)['Name']


def get_bar_address(feature):
    return get_bar_attributes(feature)['Address']


def get_bar_phone(feature):
    return get_bar_attributes(feature)['PublicPhone'][0]['PublicPhone']


def get_bar_main_info(features):
    bar_info = \
        'Name: {}\n' \
        'Address: {}\n' \
        'Phone number: {}'.format(
            get_bar_name(features),
            get_bar_address(features),
            get_bar_phone(features)
        )
    return bar_info


def get_bar_geometry(feature):
    return feature['geometry']['coordinates']


def calculate_distance(longitude1, latitude1, longitude2, latitude2):
    lon1, lat1, lon2, lat2 = map(
        radians, [longitude1, latitude1, longitude2, latitude2]
    )
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    return 2 * asin(
        sqrt(
            sin(dlat / 2) ** 2 +
            cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        )
    ) * 6367


def get_distance_to_bar(bar_data, longitude, latitude):
    bar_longitude, bar_latitude = get_bar_geometry(bar_data)
    return calculate_distance(
        bar_longitude, bar_latitude,
        longitude, latitude
    )


def fetch_data_from_web(api_key):
    response = urllib.request.urlopen(
        'https://apidata.mos.ru/v1/features/1796'
        '?api_key={}'.format(api_key)
    )
    json_data = response.read()
    return json_data


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except IOError:
        return None


def get_biggest_bar(data):
    return max(
        get_bars_features(data),
        key=lambda bar_data: get_bar_seats_count(bar_data)
    )


def get_smallest_bar(data):
    return min(
        get_bars_features(data),
        key=lambda bar_data: get_bar_seats_count(bar_data)
    )


def get_closest_bar(data, longitude, latitude):
    return min(
        get_bars_features(data),
        key=lambda bar_data: get_distance_to_bar(
            bar_data, longitude, latitude
        )
    )


if __name__ == '__main__':
    bars_info = load_data('data.json')
    if not bars_info:
        api_key = os.environ.get('MOS_RU_API_KEY')
        if not api_key:
            exit(
                'Please, set MOS_RU_API_KEY variable to fetch data about '
                'bars from web or download it from mos.ru, name received '
                'file as "data.json" and move it to the script directory'
            )
        bars_data = fetch_data_from_web(api_key)
        if not bars_data:
            exit('Connection problems')
        with open('data.json', 'wb') as file:
            file.write(bars_data)
        bars_info = json.loads(bars_data, encoding='utf-8')

    try:
        longitude, latitude = [
            float(number) for number in input(
                'Enter a longitude and a latitude: '
            ).split()
        ]
        biggest = get_biggest_bar(bars_info)
        smallest = get_smallest_bar(bars_info)
        closest = get_closest_bar(bars_info, longitude, latitude)
        print('The biggest bar')
        print(get_bar_main_info(biggest))
        print('The smallest bar')
        print(get_bar_main_info(smallest))
        print('The closest bar')
        print(get_bar_main_info(closest))
    except ValueError:
        exit('Check input data')
