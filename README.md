## Shelly data store
Scrape Shelly cloud API for storage to Postgres.

### Configuration
`database.ini`:
```ini
[postgresql]
host=<uri>
port=<port>
database=<database>
user=<user>
password=<password>
```

`shelly_config.ini`
```ini
[config]
endpoint=<shelly API endpoint<
auth_key=<auth key>

[devices]
<device_name0>=<device_id0>
...
<device_nameN>=<device_idN>
```
