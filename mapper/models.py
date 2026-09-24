from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class FinishedStat:
    time: datetime
    elapsed: timedelta
    success: bool

    def start_time(self):
        return self.time - self.elapsed
    def end_time(self):
        return self.time
    def duration(self):
        return self.elapsed
