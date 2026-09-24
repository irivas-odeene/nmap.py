from datetime import datetime, timedelta

from mapper.models import FinishedStat


def finished_stat(root):
    attrib = root.attrib

    return FinishedStat(
        time = datetime.fromtimestamp(int(attrib['time'])),
        elapsed = timedelta(seconds=float(attrib['elapsed'])),
        success = attrib['exit'] == 'success'
    )