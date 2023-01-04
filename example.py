import asyncio
import logging
from sys import argv

from growattRS232 import GrowattRS232

class TestRegs:
    registers = []
    
# defaults
# USB port of RS232 converter
DEFAULT_PORT = "/dev/ttyUSB0"
# Growatt modbus address
DEFAULT_ADDRESS = 0x1

logging.basicConfig(level=logging.DEBUG)

port = str(argv[1]) if len(argv) > 1 else DEFAULT_PORT
address = int(argv[2]) if len(argv) > 2 else DEFAULT_ADDRESS
growattRS232 = GrowattRS232(port, address)

rir1 = TestRegs()
rir1.registers = [1, 0, 232, 1509, 0, 0, 159, 1151, 0, 0, 73, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 221, 4997, 2317, 2, 0, 278, 0, 0, 0, 0, 0, 0, 0, 0, 2317, 0, 0, 0, 8, 0, 6793, 136, 31879, 0, 4, 0, 3783, 0, 4, 0, 3347, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7130]
rir1.registers = [1, 0, 68, 855, 0, 0, 66, 674, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, 4998, 2308, 1, 0, 149, 0, 0, 0, 0, 0, 0, 0, 0, 2308, 0, 0, 0, 8, 0, 6793, 136, 34393, 0, 4, 0, 3783, 0, 4, 0, 3347, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7130]
data = growattRS232.input_regs_to_data(rir1)
print(f"Sensors data: {data}")
# exit()
data = growattRS232.sync_update()
print(f"Sensors data: {data}")

