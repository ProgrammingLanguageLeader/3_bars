import requests
import os
import argparse


def fetch_data_from_web(api_key):
    try:
        params = {
            'api_key': api_key
        }
        response = requests.get(
            'https://apidata.mos.ru/v1/features/1796',
            params=params
        )
        json_data = response.content
        return json_data
    except requests.RequestException:
        return None


def save_data(json_data, save_path):
    try:
        with open(save_path, 'wb') as file:
            file.write(json_data)
        return True
    except IOError:
        return None


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A script that enables you to download bars data '
                    'from apidata.mos.ru is a simple way'
    )
    parser.add_argument(
        'save_path',
        default='data.json',
        help='A path where fetched data will be saved'
    )
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
    save_path = arguments.save_path
    api_key = os.environ.get('MOS_RU_API_KEY')
    if not api_key:
        exit('Please, set MOS_RU_API_KEY variable')
    bars_data = fetch_data_from_web(api_key)
    if not bars_data:
        exit('Connection problems')
    if not save_data(bars_data, save_path):
        exit('Unable to write to {}'.format(save_path))
    print('Saved to {}'.format(save_path))
