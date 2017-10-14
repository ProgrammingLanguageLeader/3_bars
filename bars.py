import json
import argparse
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
        'Name:          {}\n' \
        'Address:       {}\n' \
        'Phone number:  {}'.format(
            get_bar_name(features),
            get_bar_address(features),
            get_bar_phone(features)
        )
    return bar_info


def get_bar_geometry(feature):
    return feature['geometry']['coordinates']


def calculate_distance(longitude1, latitude1, longitude2, latitude2):
    earth_radius = 6367
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
    ) * earth_radius


def get_distance_to_bar(bar_data, longitude, latitude):
    bar_longitude, bar_latitude = get_bar_geometry(bar_data)
    return calculate_distance(
        bar_longitude, bar_latitude,
        longitude, latitude
    )


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except IOError:
        return None


def get_biggest_bar(bars_data):
    return max(
        get_bars_features(bars_data),
        key=lambda bar_data: get_bar_seats_count(bar_data)
    )


def get_smallest_bar(bars_data):
    return min(
        get_bars_features(bars_data),
        key=lambda bar_data: get_bar_seats_count(bar_data)
    )


def get_closest_bar(bars_data, longitude, latitude):
    return min(
        get_bars_features(bars_data),
        key=lambda bar_data: get_distance_to_bar(
            bar_data, longitude, latitude
        )
    )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A program which finds the biggest, the smallest '
                    'or the nearest bar in Moscow'
    )
    parser.add_argument(
        'data_path',
        help='A file which contains JSON information about bars'
    )
    return parser.parse_args()


def parse_coordinates(coord_string):
    try:
        longitude, latitude = map(float, coord_string.split())
        return longitude, latitude
    except (TypeError, ValueError):
        return None, None


if __name__ == '__main__':
    arguments = parse_arguments()
    data_path = arguments.data_path
    bars_data = load_data(data_path)
    if not bars_data:
        exit(
            'Unable to read {}\n'
            'To download it try to use download_bars_data.py script'.format(
                data_path
            )
        )
    longitude, latitude = parse_coordinates(
        input('Enter a longitude and a latitude: ')
    )
    if not longitude or not latitude:
        exit('Check input data')
    biggest = get_biggest_bar(bars_data)
    smallest = get_smallest_bar(bars_data)
    closest = get_closest_bar(bars_data, longitude, latitude)
    print('The biggest bar')
    print(get_bar_main_info(biggest))
    print('The smallest bar')
    print(get_bar_main_info(smallest))
    print('The closest bar')
    print(get_bar_main_info(closest))
