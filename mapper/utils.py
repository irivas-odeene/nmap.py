from datetime import datetime, timedelta
from xml.etree.ElementTree import Element


"""
Utilidades para trabajar con fechas y horas a través de datetime en python:
"""
timestamp_to_datetime = lambda t: datetime.fromtimestamp(int(t))
seconds_to_timedelta = lambda s: timedelta(seconds=float(s))
string_to_datetime = lambda s: datetime.strptime(s, '%c')
# datetime_to_str = lambda d: d.strftime('%A, %d de %b de %Y, a las %H:%M')
datetime_to_str = lambda d: d.strftime('%c')

def dict_to_kwargs(d: dict, attrib: Element) -> dict:
    """Generar un diccionario de parámetros por nombre a partir de un subarbol

    Dado un diccionario con tantas claves como argumentos con nombre tendrá la
    función, permite recuperarlos y transformarlos fácilmente a partir del
    subárbol XML indicado.

    Se las claves pueden ser:
        - Una tupla con una función a aplicar y el nombre del atributo xml
        - Una cadena, que indica el nombre del atributo xml
        - Un tipo, de forma que el atributo será la clave y se transformará a ese tipo
            - En este caso, si la clave no existe, no se creará el parámetro
        - Si el valor no existe como atributo, no se creará el parámetro
        - Finalmente, y si la entrada es otro objeto, ese será el parámetro
    """
    missing = []    # Parámetros a eliminar

    for key, act in d.items():
        if type(act) == tuple:
            # Una tupla. Aplicar act() al atributo que se llama como la clave
            d[key] = act[0](attrib[act[1]])
        elif type(act) == str:
            # Una cadena. Buscar el atributo que se llama así
            d[key] = attrib[act]
        elif type(act) == type:
            # Un tipo. Si existe, convertir el atributo con ese nombre al tipo
            if key not in attrib:
                missing.append(key)
                continue
            d[key] = act(attrib[key])
        elif act is None:
            # None. Debemos eliminar este parámetro
            missing.append(key)
        else:
            # Otros objectos. Será el valor del parámetro
            d[key] = act

    # Eliminar las claves marcadas como inexistentes
    for key in missing:
        del d[key]

    return d


def create_from_tag(root: Element, tagname: str, object_class: object) -> object:
    """Dado un subarbol, el tipo de etiquetas y la clase, crear los objetos correspondientes

    root : element
        Raíz del subarbol en el que buscar `tagname`
    tagname : str
        Etiqueta con la que crear el objeto
    object_class : object
        Clase del objeto a crear a partir de su método parse()

    returns
    -------
    object: objeto creado a partir del método parse()
    """
    subtree = root.find(tagname)

    if subtree is None:
        return None

    return object_class.parse(subtree)


def create_from_list(root: Element, tagname: str, object_class: object) -> list[object]:
    """Dado un subarbol, el tipo de etiquetas  la clase, crear la lista de objetos correspondiente

    root : element
        Raíz del subarbol en el que buscar `tagname`
    tagname : str
        Etiqueta con la que crear el objeto
    object_class : object
        Clase del objeto a crear a partir de su método parse()

    returns
    -------
    list[object]: lista de objetos creados a partir de los métodos parse()
    """
    children = root.findall(tagname)

    return [object_class.parse(child) for child in children]
