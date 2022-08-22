# speedtest-wrapper

A simple wrapper for automating Ookla Speedtest CLI runs.

## Usage

Install speedtest and schedule a cron job to run `main.py` as needed.
Make sure your `PATH` contains the location of the `speedtest` binary.

```
crontab:
# m h  dom mon dow   command
PATH=$PATH:/directory/containing/speedtest/
0 * * * * /usr/bin/python3 /path/to/main.py
```

The `main.py` script will save raw data and error logs
to `~/data` by default.

## Future Plans

The user may wish to load the raw data into a more structured data store.
Before implementing this functionality, I need to collect lots of raw data
to better understand its features and plan the logic of the data load.

## License

Released under the MIT license.
