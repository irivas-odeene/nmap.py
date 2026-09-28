from dataclasses import dataclass

from mapper.utils import *


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
