from dataclasses import dataclass
from xml.etree.ElementTree import Element

from mapper.models.host import Host, HostHint
from mapper.models.stats import RunStats
from mapper.utils import *


@dataclass
class Scan:
    """Escaneo con Nmap a alto nivel

    Este objeto representa la información de un escaneo con Nmap representado con
    clases de Python.

    start : datetime
        Fecha de inicio del escaneo
    version : str
        Versión de nmap que realizó el escaneo
    xmlversion : str
        Versión de la salida XML de nmap
    """
    # -- atributos
    start: datetime
    version: str
    xmlversion: str
    # -- hijos
    verbose: Verbose
    debugging: Debugging
    runstats: RunStats
    # -- elementos opcionales
    scaninfo: ScanInfo = None
    hosthint: HostHint = None
    hosts: list[Host] = None

    def __str__(self):
        return f"NMap versión {self.version}, escaneado el {datetime_to_str(self.start)}"

    def get_host(self, addr: str):
        for host in self.hosts:
            if host.addres.addr == addr:
                return host
        return None

    def parse(root: Element) -> object:
        kwargs = {
            'start': (timestamp_to_datetime, 'start'),
            'version': 'version',
            'xmlversion': 'xmloutputversion',
            'scaninfo': create_from_tag(root, 'scaninfo', ScanInfo),
            'verbose': create_from_tag(root, 'verbose', Verbose),
            'debugging': create_from_tag(root, 'debugging', Debugging),
            'hosthint': create_from_tag(root, 'hosthint', HostHint),
            'hosts': create_from_list(root, 'host', Host),
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
