from dataclasses import dataclass
from datetime import datetime, timedelta

from mapper.utils import *


@dataclass
class Scan:
    # -- atributos
    start: datetime
    version: str
    xmlversion: str
    # -- hijos
    scaninfo: ScanInfo
    verbose: Verbose
    debugging: Debugging
    hosthint: HostHint
    host: Host
    runstats: RunStats

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
            'hosthint': create_from_tag(root, 'hosthint', HostHint),
            'host': create_from_tag(root, 'host', Host),
            'runstats': create_from_tag(root, 'runstats', RunStats)
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
    addresses: list[Address]
    # hostnames?

    def parse(root):
        kwargs = {
            'status': create_from_tag(root, 'status', Status),
            'addresses': create_from_list(root, 'address', Address)
        }
        return HostHint(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Host:
    start: datetime
    end: datetime
    status: Status
    addresses: list[Address]
    # hostnames?
    ports: list[Port]
    os: OperatingSystem
    uptime: Uptime
    tcpsequence: TCPSequence
    ipidsequence: Sequence
    tcptssequence: Sequence
    times: Times
    distance: int = None

    def duration(self):
        return self.end - self.start

    def parse(root):
        kwargs = {
            'start': (timestamp_to_datetime, 'starttime'),
            'end': (timestamp_to_datetime, 'endtime'),
            'status': create_from_tag(root, 'status', Status),
            'addresses': create_from_list(root, 'address', Address),
            'ports': create_from_list(root.find('ports'), 'port', Port),
            'os': create_from_tag(root, 'os', OperatingSystem),
            'uptime': create_from_tag(root, 'uptime', Uptime),
            'tcpsequence': create_from_tag(root, 'tcpsequence', TCPSequence),
            'ipidsequence': create_from_tag(root, 'ipidsequence', Sequence),
            'tcptssequence': create_from_tag(root, 'tcptssequence', Sequence),
            'times': create_from_tag(root, 'times', Times)
        }
        host = Host(**dict_to_kwargs(kwargs, root.attrib))
        host.distance = int(root.find('distance').attrib['value'])
        return host


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
class Address:
    addr: str
    addr_type: str
    vendor: str = None

    def parse(root):
        kwargs = {
            'addr': str,
            'addr_type': 'addrtype',
            'vendor': str
        }
        return Address(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Port:
    protocol: str
    portnumber: int
    state: State
    service: Service = None

    def parse(root):
        kwargs = {
            'protocol': str,
            'portnumber': (int, 'portid'),
            'state': create_from_tag(root, 'state', State),
            'service': create_from_tag(root, 'service', Service)
        }
        return Port(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class State:
    state: str
    reason: str
    reason_ttl: int
    # reason_ip?

    def parse(root):
        kwargs = {
            'state': str,
            'reason': str,
            'reason_ttl': int
        }
        return State(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Service:
    name: str
    method: str
    conf: int
    # tunnel?
    # proto?
    # rpcnum?
    # lowver?
    # highver?
    # ...

    def parse(root):
        kwargs = {
            'name': str,
            'method': str,
            'conf': int
        }
        return Service(**dict_to_kwargs(kwargs, root.attrib))


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


@dataclass
class PortUsed:
    state: str
    proto: str
    portid: int

    def parse(root):
        kwargs = {
            'state': str,
            'proto': str,
            'portid': int
        }
        return PortUsed(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class OperatingSystem:
    used_ports: list[PortUsed]
    match: OperatingSystemMatch

    def parse(root):
        kwargs = {
            'used_ports': create_from_list(root, 'portused', PortUsed),
            'match': create_from_tag(root, 'osmatch', OperatingSystemMatch)
        }
        return OperatingSystem(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class OperatingSystemMatch:
    name: str
    accuracy: int
    line: int
    os_class: OperatingSystemClass

    def parse(root):
        kwargs = {
            'name': str,
            'accuracy': str,
            'line': int,
            'os_class': create_from_tag(root, 'osclass', OperatingSystemClass)
        }
        return OperatingSystemMatch(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class OperatingSystemClass:
    os_type: str
    vendor: str
    family: str
    gen: str
    accuracy: int
    cpe: str = None

    def parse(root):
        kwargs = {
            'os_type': 'type',
            'vendor': str,
            'family': 'osfamily',
            'gen': 'osgen',
            'accuracy': int
        }
        os_class = OperatingSystemClass(**dict_to_kwargs(kwargs, root.attrib))
        os_class.cpe = root.find('cpe').text
        return os_class


@dataclass
class Uptime:
    seconds: datetime
    lastboot: datetime

    def parse(root):
        kwargs = {
            'seconds': (seconds_to_timedelta, 'seconds'),
            'lastboot': (string_to_datetime, 'lastboot')
        }
        return Uptime(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class TCPSequence:
    index: int
    difficulty: str
    values: str

    def parse(root):
        kwargs = {
            'index': int,
            'difficulty': str,
            'values': str
        }
        return TCPSequence(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Sequence:
    sequence_class: str
    values: str

    def parse(root):
        kwargs = {
            'sequence_class': 'class',
            'values': str
        }
        return Sequence(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Times:
    srtt: int
    rttvar: int
    to: int

    def parse(root):
        kwargs = {
            'srtt': int,
            'rttvar': int,
            'to': int
        }
        return Times(**dict_to_kwargs(kwargs, root.attrib))

@dataclass
class RunStats:
    finished: datetime
    host_stats: HostStats

    def summary(self):
        return f"Nmap done at {datetime_to_str(self.finished)}; {self.host_stats.total()} hosts found ({self.host_stats.up} host up)"

    def parse(root):
        return RunStats(
            finished = timestamp_to_datetime(root.find('finished').attrib['time']),
            host_stats = create_from_tag(root, 'hosts', HostStats)
        )


@dataclass
class HostStats:
    up: int
    down: int

    def total(self):
        return self.up + self.down

    def parse(root):
        kwargs = {
            'up': int,
            'down': int
        }
        return HostStats(**dict_to_kwargs(kwargs, root.attrib))
