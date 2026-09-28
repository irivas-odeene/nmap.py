from dataclasses import dataclass

from mapper.models.operating_system import OperatingSystem
from mapper.models.port import Port
from mapper.utils import *


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
