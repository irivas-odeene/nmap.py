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
    scaninfo : ScanInfo|None
            [Opcional] Información general sobre el tipo de escaneo
    verbose : Verbose
        Información sobre el nivel de logging
    debugging : Debugging
        Información sobre el nivel de logging
    hosthint : HostHint|None
        [Opcional] Resumen de los equipos descubiertos
    hosts : list[Host]|None
        [Opcional] Equipos descubiertos
    runstats : RunStats
        Estadísticas sobre la ejecución

    Sin implementar: target, taskbegin, taskprogress, taskend, prescript, postscript, output
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
    scaninfo: ScanInfo|None = None
    hosthint: HostHint|None = None
    hosts: list[Host]|None = None

    def __str__(self):
        return f"NMap version {self.version}, scanned on {datetime_to_str(self.start)}"

    def get_host(self, addr: str) -> Host|None:
        """Buscar un host entre los descubiertos por su dirección IP o MAC

        Busca entre los hosts aquel con dirección `addr` y lo devuelve

        addr : str
            Dirección del host que se busca
        """
        for host in self.hosts:
            if addr in host.addresses:
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
    """Información sobre el tipo de escaneo y los servicios descubiertos

    scan_type : str
        Tipo de escaneo: [syn, ack, bounce, connect, null, xmas, window, maimon fin, udp, sctpinit, sctpcookieecho, ipproto]
    protocol : str
        Protocolo del escaneo: [ip, tcp, udp, sctp]
    numservices : int
        Número de servicios (puertos) descubiertos
    services : str
        Rangos de puertos escaneados
    """
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
    """Nivel de detalle de la salida del escaneo"""
    level: int

    def parse(root):
        return Verbose(**dict_to_kwargs({'level': int}, root.attrib))


@dataclass
class Debugging:
    """Nivel de detalle de la salida del escaneo"""
    level: int

    def parse(root):
        return Debugging(**dict_to_kwargs({'level': int}, root.attrib))
