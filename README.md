# speedtest-wrapper

A simple wrapper for automating Ookla Speedtest CLI runs.

## Usage

Install speedtest and schedule a cron job to run `main.py` as needed.
The script will save raw data and error logs to `~/data` by default.

## Future Plans

The user may wish to load the raw data into a more structured data store.
Before implementing this functionality, I need to collect lots of raw data
to better understand its features and plan the logic of the data load.

## License

Released under the MIT license.
