from datetime import datetime, timedelta


timestamp_to_datetime = lambda t: datetime.fromtimestamp(int(t))
seconds_to_timedelta = lambda s: timedelta(seconds=float(s))

def dict_to_kwargs(d, attrib):
    print(attrib)
    for key, act in d.items():
        if type(act) == tuple:
            d[key] = act[0](attrib[act[1]])

    return d