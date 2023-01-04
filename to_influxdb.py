#!/usr/bin/python3
import asyncio
import logging
from sys import argv

from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from growattRS232 import GrowattRS232, ModbusException
from growattRS232.const import *

api_token = "G--VXX0UE9H1VCWYv42mum-GTGmjjrgeVHwpl5r-GS6jGwMwD_M7iUR2qay5x3YP_5dboGOTyYXnXGvV3tw_Hg=="
org = "rwassens"
bucket = "domo_bucket"
client = InfluxDBClient(url="http://rwassens-domo.ddns.net:8086/", token=api_token, org=org, debug=True, timeout=2000)

# defaults
# USB port of RS232 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1


class TestRegs:
    registers = []
    
    
logging.basicConfig(level=logging.DEBUG)

port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
growattRS232 = GrowattRS232(port, address)

# rir1 = TestRegs()
# rir1.registers = [1, 0, 68, 855, 0, 0, 66, 674, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, 4998, 2308, 1, 0, 149, 0, 0, 0, 0, 0, 0, 0, 0, 2308, 0, 0, 0, 8, 0, 6793, 136, 34393, 0, 4, 0, 3783, 0, 4, 0, 3347, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7130]
# data = growattRS232.input_regs_to_data(rir1)

try:
    data = growattRS232.sync_update()
except ModbusException as e:
    logging.debug(f"ERROR:{e}\nAssume Growatt inverter is powered off, exit")
    exit()
    
# print(f"Sensors data: {data}")

points = [{
    "measurement": "BJK4CDJ0AK",
    "fields": {                        
        "pv1_power": data[ATTR_INPUT_1_POWER],
        "pv1_today": data[ATTR_INPUT_1_ENERGY_TODAY],
        "pv1_total": data[ATTR_INPUT_1_ENERGY_TOTAL],
        "pv2_power": data[ATTR_INPUT_2_POWER],
        "pv2_today": data[ATTR_INPUT_2_ENERGY_TODAY],
        "pv2_total": data[ATTR_INPUT_2_ENERGY_TOTAL],
        "pv_power": data[ATTR_INPUT_POWER],
        "pv_today": data[ATTR_INPUT_ENERGY_TODAY],
        "pv_total": data[ATTR_INPUT_ENERGY_TOTAL],
        "status": data[ATTR_STATUS],
        "status_num": data[ATTR_STATUS_CODE],
    }
}]

write_client = client.write_api(write_options=SYNCHRONOUS)
write_client.write(bucket=bucket, record=points)

