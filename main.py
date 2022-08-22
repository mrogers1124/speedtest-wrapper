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


# Run speedtest, returning the CompletedProcess object
def run_speedtest() -> subprocess.CompletedProcess:
    result = subprocess.run(['speedtest', '--format=json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result


def process_result(result: subprocess.CompletedProcess) -> None:
    # Was the speedtest a success or failure?
    if result.returncode:
        output: bytes = result.stderr
    else:
        output: bytes = result.stdout

    # Extract the JSON formatted data from the process output
    output_str = output.decode()
    data_str = re.search(r'(?s)\{.*}', output_str)[0]
    data = json.loads(data_str)

    # Get the timestamp from the JSON formatted data
    timestamp = data['timestamp']

    # Save JSON formatted data in raw folder
    fn_raw = str(timestamp) + '.json'
    fp_raw = os.path.join(rawpath, fn_raw)
    with open(fp_raw, 'w') as file:
        file.write(data_str)

    # If process was unsuccessful, save the entire output to the error log
    if result.returncode:
        fn_raw = str(timestamp) + '.log'
        fp_error = os.path.join(errorpath, fn_raw)
        with open(fp_error, 'w') as file:
            file.write(output_str)


if __name__ == '__main__':
    result = run_speedtest()
    process_result(result)
