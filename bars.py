import json
import argparse
from math import asin
from math import sin
from math import cos
from math import sqrt
from math import radians


def get_bars_features_list(bars_data):
    return bars_data['features']


def get_bar_attributes(bar_data):
    return bar_data['properties']['Attributes']


def get_bar_seats_count(bar_data):
    return get_bar_attributes(bar_data)['SeatsCount']


def get_bar_main_info_string(bar_data):
    attributes = get_bar_attributes(bar_data)
    info_string = \
        'Name:          {}\n' \
        'Address:       {}\n' \
        'Phone number:  {}'.format(
            attributes['Name'],
            attributes['Address'],
            attributes['PublicPhone'][0]['PublicPhone']
        )
    return info_string


def get_bar_coordinates(features):
    return features['geometry']['coordinates']


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


def get_distance_to_bar(bar_features, longitude, latitude):
    bar_longitude, bar_latitude = get_bar_coordinates(bar_features)
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


def get_biggest_bar(bars_features):
    return max(
        bars_features,
        key=get_bar_seats_count
    )


def get_smallest_bar(bars_features):
    return min(
        bars_features,
        key=get_bar_seats_count
    )


def get_closest_bar(bars_features, longitude, latitude):
    return min(
        bars_features,
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
    bars_features = get_bars_features_list(bars_data)
    longitude, latitude = parse_coordinates(
        input('Enter a longitude and a latitude: ')
    )
    if not longitude or not latitude:
        exit('Check input data')
    biggest = get_biggest_bar(bars_features)
    smallest = get_smallest_bar(bars_features)
    closest = get_closest_bar(bars_features, longitude, latitude)
    print('The biggest bar')
    print(get_bar_main_info_string(biggest))
    print('The smallest bar')
    print(get_bar_main_info_string(smallest))
    print('The closest bar')
    print(get_bar_main_info_string(closest))
