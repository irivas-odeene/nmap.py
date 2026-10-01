from argparse import ArgumentParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from mapper import models
from mapper.inspect import avisos


parser = ArgumentParser(
    prog = "nmap.py",
    description="NMap interface library for Python"
)
parser.add_argument('filename')
args = parser.parse_args()

path = Path(args.filename)
if not path.exists():
    print("\033[91;3mError:\033[0m The path doesn't exist.")
    sys.exit(1)
if not path.exists() or not path.is_file():
    print("\033[91;3mError:\033[0m Invalid path. Should be a file.")
    sys.exit(1)


try:
    tree = ET.parse(path)
except ET.ParseError:
    print("\033[91;3mError:\033[0m Invalid XML file")
    sys.exit(1)

root = tree.getroot()

reglas = [
    (
        [21, 'ftp', 23, 'telnet', 80, 'http'],
        'Protocolo no cifrado. Se recomienda utilizar variantes cifradas.',
        'aviso'
    ),
    (
        [22, 'ssh', 3389, 'rdp'],
        'Servicio de administración. Revisa las reglas de autenticación para evitar problemas de seguridad.',
        'aviso'
    ),
    (
        [445, 'smb', 139, 'netbios-ssh'],
        'Servicio de compartición de archivos. No debería de estar expuesto.',
        'error'
    ),
    (
        [3306, 'mysql', 5432, 'postgresql', 270127, 'mongodb'],
        'Base de Datos expuesta.',
        'error'
    ),
]

scan = models.Scan.parse(root)
print(scan)
# breakpoint()
avisos(scan, reglas)
