from datetime import datetime, timedelta


timestamp_to_datetime = lambda t: datetime.fromtimestamp(int(t))
seconds_to_timedelta = lambda s: timedelta(seconds=float(s))

def dict_to_kwargs(d, attrib):
    for key, act in d.items():
        if type(act) == tuple:
            d[key] = act[0](attrib[act[1]])
        elif type(act) == type:
            d[key] = attrib[act]
        else:
            d[key] = act

    return d

datetime_to_str = lambda d: d.strftime('%A, %d de %b de %Y, a las %H:%M')

def create_from_tag(root, tagname, object_class):
    subtree = root.find(tagname)

    return object_class.parse(subtree)

