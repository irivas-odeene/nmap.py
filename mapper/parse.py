from mapper.models import FinishedStat
from mapper.utils import timestamp_to_datetime, seconds_to_timedelta, dict_to_kwargs

def finished_stat(root):
    attrib = root.attrib

    kwargs = {
        'time': (timestamp_to_datetime, 'time'),
        'elapsed': (seconds_to_timedelta, 'elapsed'),
        'success': attrib['exit'] == 'success'
    }

    kwargs = dict_to_kwargs(kwargs, attrib)
    return FinishedStat(**kwargs)