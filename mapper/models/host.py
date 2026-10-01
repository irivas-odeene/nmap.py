from dataclasses import dataclass

from mapper.models.operating_system import OperatingSystem
from mapper.models.port import Port
from mapper.utils import *


@dataclass
class HostHint:
    """Detalles de alto nivel sobre los hosts descbiertos

    status : Status
        Estado del host
    addresses : Address
        Direcciones del host
    hostnames : str|None
        [Opcional] Si se conoce, hostname del equipo
    """
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
    """Detalles sobre un host

    start : datetime
        Fecha y hora del inicio del escaneo del host
    end : datetime
        Fecha y hora del fin del escaneo del host
    status : Status
        Estado del host
    addresses : list[Address]
        Dirección o direcciones del host
    hostnames : str|None (sin implementar)
        [Opcional] Hostnames del equipo
    ports : list[Port]|None
        Lista de puertos abiertos en el equipo
    os : OperatingSystem|None
        [Opcional] Información descubierta sobre el sistema operativo del equipo
    distance : int|None
        [Opcional] Distancia del equipo (número de saltos)
    uptime : int|None
        [Opcional] Tiempo de funcionamiento del equipo desde el último inicio
    tcpsequence : TCPSequence|None
        [Opcional] ...
    ipidsequence : Sequence|None
        [Opcional] ...
    tcptssequence : Sequence|None
        [Opcional] ...
    hostscript : HostScript|None
        [Opcional]
    trace : Trace|None
        [Opcional] Traceroute entre el host que escanea y el escaneado
    times : Times|None
        [Opcional] ...

    Sin implementar: smurf, hostscript, trace
    """
    start: datetime
    end: datetime
    status: Status
    addresses: list[Address]
    # hostnames?
    ports: list[Port]|None = None
    os: OperatingSystem|None = None
    distance: int = None
    uptime: Uptime|None = None
    tcpsequence: TCPSequence|None = None
    ipidsequence: Sequence|None = None
    tcptssequence: Sequence|None = None
    hostscripts: HostScript|None = None
    trace: Trace|None = None
    times: Times|None = None

    def duration(self) -> timedelta:
        """Duración del escaneo para el equipo"""
        return self.end - self.start

    def find(self, x):
        for port in self.ports:
            if type(x) == int and port.portnumber == x:
                return port
            elif type(x) == str and port.service is not None:
                if port.service.name == x:
                    return port

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
            'hostscripts': create_from_tag(root, 'hostscript', HostScript),
            'trace': create_from_tag(root, 'trace', Trace),
            'times': create_from_tag(root, 'times', Times)
        }
        return Host(**dict_to_kwargs(kwargs, root.attrib),
                    distance=int(root.find('distance').attrib['value']))


@dataclass
class Status:
    """Información sobre el estado del equipo"""
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
    """Dirección IP o MAC"""
    addr: str
    addr_type: str
    vendor: str|None = None

    def __eq__(self, addr: str|Address) -> bool:
        """Comparar con otra dirección IP"""
        if type(addr) == Address:
            return self.addr == addr.addr and self.addr_type == addr.addr_type

        return self.addr == addr

    def parse(root):
        kwargs = {
            'addr': str,
            'addr_type': 'addrtype',
            'vendor': str
        }
        return Address(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class Uptime:
    """Información sobre el tiempo de ejecución del equipo

    seconds : timedelta
        Segundos que han pasado desde que el equipo arrancó por última vez
    lastboot : datetime
        Momento en el que el equipo arrancó por última vez

    (los valores se corresponden al momento en el que nmap escaneó al equipo)
    """
    seconds: timedelta
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
class HostScript:
    scripts: list[Script]

    def parse(root):
        return HostScript(**{'scripts': create_from_list(root, 'script', Script)})


@dataclass
class Script:
    script_id: str
    output: str
    value: str|None = None

    def parse(root):
        kwargs = {
            'script_id': 'id',
            'output': str,
        }
        return Script(**dict_to_kwargs(kwargs, root.attrib),
                      value = root.text)


@dataclass
class Trace:
    """Ruta entre el host que escanea y el escaneado

    hops : list[Hop]|None
        [Opcional] Saltos entre ambos hosts
    """
    hops: list[Hop]|None = None

    def parse(root):
        return Trace(hops = create_from_list(root, 'hop', Hop))


@dataclass
class Hop:
    """Salto. Representa un router por el que pasan los paquetes

    ttl : int
        TTL restante en los paquetes
    ipaddr : str
        Dirección IP del router
    rtt : float
        RoundTripTime, latencia
    host : str|None
        [Opcional] Hostname del router
    """
    ttl: int
    ipaddr: str
    rtt: float
    host: str|None = None

    def parse(root):
        kwargs = {
            'ttl': int,
            'ipaddr': str,
            'rtt': float,
            'host': str
        }
        return Hop(**dict_to_kwargs(kwargs, root.attrib))



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
