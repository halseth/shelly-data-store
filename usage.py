import datetime
import time

from database import get_device_status
from config import load_config
from main import energy_and_ts

if __name__ == '__main__':
    pg_config = load_config()

    shelly_config = load_config(filename="shelly_config.ini", section="config")
    print(shelly_config)
    shelly_devices = load_config(filename="shelly_config.ini", section="devices")
    print(shelly_devices)

    for device_name in shelly_devices:
        device_id = shelly_devices[device_name]

        past = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
        print(f"fetching {device_name}({device_id}) since {past}")

        rows = get_device_status(pg_config, device_id, past)
        (energy_start, ts_start) = energy_and_ts(rows[0][4])
        (energy_end, ts_end) = energy_and_ts(rows[-1][4])

        energy_delta = energy_end - energy_start
        time_delta = ts_end - ts_start
        elapsed = datetime.timedelta(seconds=time_delta)

        avg_power = energy_delta / (elapsed.seconds / 60 / 60)
        print(f"{device_name}: energy_delta={energy_delta}, elapsed={elapsed}, avg_power={avg_power}")



