from datetime import datetime, timedelta


timestamp_to_datetime = lambda t: datetime.fromtimestamp(int(t))
seconds_to_timedelta = lambda s: timedelta(seconds=float(s))
string_to_datetime = lambda s: datetime.strptime(s, '%c')

def dict_to_kwargs(d, attrib):
    missing = []

    for key, act in d.items():
        if type(act) == tuple:
            d[key] = act[0](attrib[act[1]])
        elif type(act) == str:
            d[key] = attrib[act]
        elif type(act) == type:
            if key not in attrib:
                missing.append(key)
                continue
            d[key] = act(attrib[key])
        elif act is None:
            missing.append(key)
        else:
            d[key] = act

    for key in missing:
        del d[key]

    return d

datetime_to_str = lambda d: d.strftime('%A, %d de %b de %Y, a las %H:%M')

def create_from_tag(root, tagname, object_class):
    subtree = root.find(tagname)

    return None if subtree is None else object_class.parse(subtree)

def create_from_list(root, tagname, object_class):
    children = root.findall(tagname)

    return [object_class.parse(child) for child in children]
