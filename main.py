import time

import requests

from config import load_config
from database import insert_device_status

def get_devices_status(device_id):
    url = shelly_config['endpoint'] + '/device/status'
    key = shelly_config['auth_key']
    params = {'id': device_id, 'auth_key': key}

    x = requests.post(url, params=params)
    return x

def update_device_statuses(pg_config, shelly_devices):
    for device_name in shelly_devices:
        device_id = shelly_devices[device_name]
        status = get_devices_status(device_id)
        dict = status.json()
        insert_device_status(pg_config, device_id, device_name, status.text)
        (total, ts) = energy_and_ts(dict)
        print(f"inserted {device_name}({device_id}) total_energy={total} at {ts}")

def energy_and_ts(dict):
    aenergy = dict['data']['device_status']['switch:0']['aenergy']
    total = aenergy['total']
    ts = aenergy['minute_ts']

    return (total, ts)


if __name__ == '__main__':
    pg_config = load_config()

    shelly_config = load_config(filename="shelly_config.ini", section="config")
    print(shelly_config)
    shelly_devices = load_config(filename="shelly_config.ini", section="devices")
    print(shelly_devices)

    while True:
        update_device_statuses(pg_config, shelly_devices)
        time.sleep(30)