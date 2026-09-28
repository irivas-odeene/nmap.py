from dataclasses import dataclass

from mapper.utils import *


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
