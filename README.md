# speedtest-wrapper

A simple wrapper for automating Ookla Speedtest CLI runs
and loading the resulting raw data into a SQLite3 database.

## Usage

Install speedtest from the [Ookla website](https://www.speedtest.net/).

This repository contains two runnable modules:
* `main.py` runs the speedtest program and saves the raw result.
* `load.py` loads the raw data into a SQLite3 database.

Schedule a cron job to run `main.py` and `load.py` as needed.
Make sure your `PATH` contains the location of the `speedtest` binary.

```
crontab:
# m h  dom mon dow   command
PATH=$PATH:/directory/containing/speedtest/
0 * * * * /usr/bin/python3 /path/to/main.py
30 0 * * * /usr/bin/python3 /path/to/load.py
```

Raw data and error logs are saved in `~/data` by default.

## License

Released under the MIT license.
