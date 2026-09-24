from argparse import ArgumentParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

# from mapper import models
from mapper import parse


parser = ArgumentParser(
    prog = "nmap.py",
    description="NMap interface library for Python"
)
parser.add_argument('filename')
args = parser.parse_args()

path = Path(args.filename)
if not path.exists():
    print("\033[91;3mError:\033[0m The path doesn't exist.")
    sys.exit(1)
if not path.exists() or not path.is_file():
    print("\033[91;3mError:\033[0m Invalid path. Should be a file.")
    sys.exit(1)


try:
    tree = ET.parse(path)
except ET.ParseError:
    print("\033[91;3mError:\033[0m Invalid XML file")
    sys.exit(1)

root = tree.getroot()

finished_stat = parse.finished_stat(root[5][0])
print(f"Executed from {finished_stat.start_time().isoformat()} to {finished_stat.end_time().isoformat()} ({finished_stat.duration().total_seconds()}s)")