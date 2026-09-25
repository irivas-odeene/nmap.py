from dataclasses import dataclass
from datetime import datetime, timedelta

from mapper.utils import *

@dataclass
class Scan:
    start: datetime
    version: str
    xmlversion: str
    scaninfo: ScanInfo
    verbose: Verbose
    debugging: Debugging
    hosthint: HostHint

    def __str__(self):
        return f"NMap versión {self.version}, escaneado el {datetime_to_str(self.start)}"

    def parse(root):
        kwargs = {
            'start': (timestamp_to_datetime, 'start'),
            'version': 'version',
            'xmlversion': 'xmloutputversion',
            'scaninfo': create_from_tag(root, 'scaninfo', ScanInfo),
            'verbose': create_from_tag(root, 'verbose', Verbose),
            'debugging': create_from_tag(root, 'debugging', Debugging),
            'hosthint': create_from_tag(root, 'hosthint', HostHint)
        }
        return Scan(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class ScanInfo:
    scan_type: str
    protocol: str
    numservices: int
    services: str

    def __str__(self):
        return f"{self.protocol.upper()} {self.scan_type} scan. Found {self.numservices} available services"

    def __repr__(self):
        return f"{self.__class__.__name__}(scan_type='{self.scan_type}', protocol='{self.protocol}', numservices={self.numservices}), services='{self.services[:15]}...'"

    def parse(root):
        kwargs = {
            'scan_type': 'type',
            'protocol': 'protocol',
            'numservices': int,
            'services': 'services'
        }
        return ScanInfo(**dict_to_kwargs(kwargs, root.attrib))

@dataclass
class Verbose:
    level: int

    def parse(root):
        return Verbose(**dict_to_kwargs({'level': int}, root.attrib))


@dataclass
class Debugging:
    level: int

    def parse(root):
        return Debugging(**dict_to_kwargs({'level': int}, root.attrib))


@dataclass
class HostHint:
    status: Status

    def parse(root):
        kwargs = {
            'status': create_from_tag(root, 'status', Status)
        }
        return HostHint(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Status:
    state: str
    reason: str
    reason_ttl: int

    def parse(root):
        kwargs = {
            'state': str,
            'reason': str,
            'reason_ttl': int
        }
        return Status(**dict_to_kwargs(kwargs, root.attrib))


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
