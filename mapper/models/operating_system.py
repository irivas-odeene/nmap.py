from dataclasses import dataclass

from mapper.models.port import CPE
from mapper.utils import *


@dataclass
class OperatingSystem:
    """Información sobre el sistema operativo e un equipo

    used_ports : list[PortUsed]|None
        [Opcional] Lista de puertos abiertos en el host
    match : list[OperatingSytemMatch]|None
        [Opcional] Lista de sistemas operativos que podría tener el host
    """
    used_ports: list[PortUsed]|None = None
    match: list[OperatingSystemMatch]|None = None

    def parse(root):
        kwargs = {
            'used_ports': create_from_list(root, 'portused', PortUsed),
            'match': create_from_list(root, 'osmatch', OperatingSystemMatch)
        }
        return OperatingSystem(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class PortUsed:
    """Resumen de la información de un puerto abierto en el sistema operativo

    state : str
        Estado del puerto: (CDATA)
    proto : str
        Protocolo del puerto: (ip, tcp, udp, sctp)
    portid : int
        Número de puerto
    """
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
class OperatingSystemMatch:
    """Coincidencia con un sistema operativo

    name : str
        Nombre del sistema operativo
    accuracy : int
        Probabilidad de coincidencia
    line : int
        ...
    os_class : list[OperatingSystemClass]|None
        [Opcional] Lista de posibles tipos de sistemas operativos para el host
    """
    name: str
    accuracy: int
    line: int
    os_class: list[OperatingSystemClass]|None = None

    def parse(root):
        kwargs = {
            'name': str,
            'accuracy': int,
            'line': int,
            'os_class': create_from_list(root, 'osclass', OperatingSystemClass)
        }
        return OperatingSystemMatch(**dict_to_kwargs(kwargs, root.attrib))


@dataclass
class OperatingSystemClass:
    """Tipo de sistema operativo

    vendor : str
        Desarrollador del sistema operativo
    accuracy : int
        Probabilidad de acierto
    family : str
        Familia del sistema operativo
    gen : str|None
        [Opcional] Versión del sistema operativo
    os_type : str|None
        [Opcional] Tipo de sistema operativo (general, de escritorio, empotrado)
    cpe : list[str]|None
        [Opcional] Resumen del sistema operativo (versión, familia...)
    """
    vendor: str
    accuracy: int
    family: str
    gen: str|None = None
    os_type: str|None = None
    cpe: list[CPE]|None = None

    def parse(root):
        kwargs = {
            'os_type': 'type',
            'vendor': str,
            'family': 'osfamily',
            'gen': 'osgen',
            'accuracy': int,
            'cpe': create_from_list(root, 'cpe', CPE)
        }
        return OperatingSystemClass(**dict_to_kwargs(kwargs, root.attrib))
