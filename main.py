
import xml.etree.ElementTree as ET

# from mapper import models
from mapper import parse


tree = ET.parse("misc/salida.xml")
root = tree.getroot()

finished_stat = parse.finished_stat(root[5][0])
print(f"Executed from {finished_stat.start_time().isoformat()} to {finished_stat.end_time().isoformat()} ({finished_stat.duration().total_seconds()}s)")