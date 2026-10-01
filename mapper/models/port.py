from dataclasses import dataclass

from mapper.utils import *


@dataclass
class Port:
    """Información sobre un puerto expuesto en una máquina

    protocol : str
        Protocolo del puerto: ()
    portnumber : int
        Número del puerto
    state : State
        Estado del puerto
    service : Service|None
        [Opcional]
    """
    protocol: str
    portnumber: int
    state: State
    service: Service = None

    def __str__(self):
        return f"{self.portnumber:>5}/{self.protocol} {self.state.state:^10} {self.service.name:<20} {self.service.version}"

    def __eq__(self, x: int|str):
        if type(x) == str:
            return x == self.service.name
        return x == self.portnumber

    def __hash__(self):
        return int(''.join([str(ord(l)) for l in self.protocol])+str(self.portnumber))

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
    """Estado de un puerto

    state : str
        Estado del puerto: (up, down, unknownm, skipped)
    reason : str
        Motivo por el que se le asignó ese estado al puerto
    reason_ttl : int
        ...
    """
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
    """Descripción de un servicio detectado en un puerto

    name : str
        Nombre del servicio
    conf : int
        Nivel de confianza en la respuesta [0-10]
    method : str
        Método de descubrimiento del servicio
    product : str|None
        [Opcional] Nombre del producto
    version : str|None
        [Opcional] Versión del servicio
    ostype : str|None
        [Opcional] Tipo de sistema operativo
    """
    name: str
    conf: int
    method: str
    # tunnel?
    # proto?
    # rpcnum?
    # lowver?
    # highver?
    # ...
    product: str|None = None
    version: str|None = None
    ostype: str|None = None
    cpe: list[CPE]|None = None

    def parse(root):
        kwargs = {
            'name': str,
            'method': str,
            'conf': int,
            'product': str,
            'version': str,
            'ostype': str,
            'cpe': create_from_list(root, 'cpe', CPE)
        }
        return Service(**dict_to_kwargs(kwargs, root.attrib))

@dataclass
class CPE:
    """Common Platform Enumeration

    Información sobre la plataforma (host o servicio). Sigue la estructura:
        cpe:/<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>

    part : str
        Tipo: a para aplicaciones, h para plataformas hardware o para sisetmas operativos
    vendor : str
        Fabricante del producto
    product : str
        Producto
    version : str
        Versión del producto
    update : str
        ...
    edition : str
        ...
    language : str
        ...
    """
    part: str|None = None
    vendor: str|None = None
    product: str|None = None
    version: str|None = None
    update: str|None = None
    edition: str|None = None
    language: str|None = None

    def parse(root):
        keys = ['part', 'vendor', 'product', 'version', 'update', 'edition', 'language']
        values = root.text[5:].split(':')
        values = [v if v != '' else None for v in values]
        values += [None] * (len(keys) - len(values))

        return CPE(**dict(zip(keys, values)))
