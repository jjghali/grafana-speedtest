from datetime import datetime
import time
import subprocess
import json
import schedule
import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

def run_speedtest():
    url = os.environ["INFLUX_URL"]
    token = os.environ["INFLUX_TOKEN"]
    org = os.environ["INFLUX_ORG"]
    bucket = os.environ["INFLUX_BUCKET"]
    
    time_now = str(datetime.now())
    print("{0} - Running speedtest".format(time_now))
    
    output = subprocess.run(["speedtest-cli","--json"], check=True, stdout=subprocess.PIPE, universal_newlines=True)

    if output.stderr is None:
        print("Pushing results to InfluxDB")
        result = json.loads(output.stdout)
        client = InfluxDBClient(url=url, token=token)
        point = Point("speedtest") \
            .field("download", result["download"]) \
            .field("upload", result["upload"]) \
            .field("ping", result["ping"]) \
            .time(result["timestamp"], WritePrecision.NS)
    
        write_api = client.write_api(write_options=SYNCHRONOUS)
    
        write_api.write(bucket, org, point)
    
        print("Test complete!")

schedule.every(30).minutes.do(run_speedtest)

print("Speedtest started...")
while True:    
    schedule.run_pending()
    time.sleep(1)