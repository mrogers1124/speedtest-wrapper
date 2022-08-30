import json
import os
import re
import subprocess

# Data paths
datapath = os.path.expanduser('~/data')
rawpath = os.path.join(datapath, 'raw')
processedpath = os.path.join(datapath, 'processed')
errorpath = os.path.join(datapath, 'error')


for path in [datapath, rawpath, processedpath, errorpath]:
    if not os.path.isdir(path):
        os.makedirs(path)


# Run speedtest, saving the raw data on success or an error log on failure
def run_speedtest() -> None:
    result = subprocess.run(['speedtest', '--format=json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # If process was unsuccessful, route the output from stderr to the error folder
    if result.returncode:
        output: bytes = result.stderr
        out_ext = '.log'
        out_dir = errorpath
    # Otherwise, route the output from stdout to the raw data folder
    else:
        output: bytes = result.stdout
        out_ext = '.json'
        out_dir = rawpath

    # Extract the JSON formatted data from the process output
    output_str = output.decode()
    data_str = re.search(r'(?s)\{.*}', output_str)[0]
    data = json.loads(data_str)

    # Get the timestamp from the JSON formatted data
    timestamp = data['timestamp']

    # Write the file
    out_fn = timestamp + out_ext
    out_fp = os.path.join(out_dir, out_fn)
    with open(out_fp, 'wb') as file:
        file.write(output)


if __name__ == '__main__':
    run_speedtest()
