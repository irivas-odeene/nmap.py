from dataclasses import dataclass

from mapper.utils import *


@dataclass
class RunStats:
    finished: datetime
    host_stats: HostStats

    def summary(self):
        return f"Nmap done at {datetime_to_str(self.finished)}; {self.host_stats.total()} hosts found ({self.host_stats.up} host up)"

    def parse(root):
        return RunStats(
            finished = timestamp_to_datetime(root.find('finished').attrib['time']),
            host_stats = create_from_tag(root, 'hosts', HostStats)
        )


@dataclass
class HostStats:
    up: int
    down: int

    def total(self):
        return self.up + self.down

    def parse(root):
        kwargs = {
            'up': int,
            'down': int
        }
        return HostStats(**dict_to_kwargs(kwargs, root.attrib))
