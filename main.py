import json
import os
import re
import subprocess

# Data paths
datapath = os.path.expanduser('~/data')
rawpath = os.path.join(datapath, 'raw')
errorpath = os.path.join(datapath, 'error')

for path in [datapath, rawpath, errorpath]:
    if not os.path.isdir(path):
        os.makedirs(path)


# Run speedtest, saving the raw data and error messages
def run_speedtest() -> None:
    result = subprocess.run(['speedtest', '--format=json-pretty'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode:
        output: bytes = result.stderr
    else:
        output: bytes = result.stdout

    output_str = output.decode()
    data_str = re.search(r'(?s)\{.*}', output_str)[0]
    data = json.loads(data_str)
    timestamp = data['timestamp']

    # Save data in raw folder
    fn_raw = str(timestamp) + '.json'
    fp_raw = os.path.join(rawpath, fn_raw)
    with open(fp_raw, 'w') as file:
        file.write(data_str)

    # Save error log
    if result.returncode:
        fn_raw = str(timestamp) + '.log'
        fp_error = os.path.join(errorpath, fn_raw)
        with open(fp_error, 'w') as file:
            file.write(output_str)


if __name__ == '__main__':
    run_speedtest()
