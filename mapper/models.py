from dataclasses import dataclass
from datetime import datetime, timedelta

from mapper.utils import *

@dataclass
class Scan:
    start: datetime
    version: str
    xmlversion: str
    scaninfo: ScanInfo

    def __str__(self):
        return f"NMap versión {self.version}, escaneado el {datetime_to_str(self.start)}"

    def parse(root):
        kwargs = {
            'start': (timestamp_to_datetime, 'start'),
            'version': 'version',
            'xmlversion': 'xmloutputversion',
            'scaninfo': create_from_tag(root, 'scaninfo', ScanInfo)
        }
        return Scan(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class ScanInfo:
    scan_type: str
    protocol: str
    numservices: int

    def __str__(self):
        return f"{self.protocol.upper()} {self.scan_type} scan. Found {self.numservices} available services"

    def parse(root):
        kwargs = {
            'scan_type': 'type',
            'protocol': 'protocol',
            'numservices': (int, 'numservices')
        }
        return ScanInfo(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class FinishedStat:
    time: datetime
    elapsed: timedelta
    success: bool

    def start_time(self):
        return self.time - self.elapsed
    def end_time(self):
        return self.time
    def duration(self):
        return self.elapsed

    def parse(root):
        kwargs = {
            'time': (timestamp_to_datetime, 'time'),
            'elapsed': (seconds_to_timedelta, 'elapsed'),
            'success': root.attrib['exit'] == 'success'
        }
        return FinishedStat(**dict_to_kwargs(kwargs, root.attrib))
