from datetime import datetime, timedelta


class FinishedStat:
    def __init__(
            self,
            time: datetime,
            elapsed: timedelta,
            success: bool
    ):
        self.time = time
        self.elapsed = elapsed
        self.success = success

    def start_time(self):
        return self.time - self.elapsed
    def end_time(self):
        return self.time
    def duration(self):
        return self.elapsed
