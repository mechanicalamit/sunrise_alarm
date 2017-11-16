

from datetime import datetime
from time import sleep
import pytz

# Enhancement, set speedup value on the fly
# That would require a convuletion on the fly and addition of deltas as we go along


class speedup_date(object):
    def __init__(self, TZ = 'US/Eastern', enable_speedup=False, speedup_val=1):
        self.enable_speedup = enable_speedup
        self.speedup_val = speedup_val

        self.TZ = pytz.timezone(TZ)

        self.start_datetime = datetime.now(tz=self.TZ)
        self.last_datetime = self.start_datetime
        self.last_speedtime = self.start_datetime
        self.cummulative_dtime = self.last_datetime - self.last_datetime # Fancy way to get zero

    def now(self):
        cur_datetime = datetime.now(tz=self.TZ)
        if not self.enable_speedup:
            return cur_datetime

        # Convolution, so since last time we were called
        d_time = cur_datetime - self.last_datetime
        sp_d_time = d_time * self.speedup_val
        self.last_speedtime = self.last_speedtime + sp_d_time
        self.last_datetime = cur_datetime
        return self.last_speedtime

    def get_last_speed_stamp(self):
        if not self.enable_speedup:
            return datetime.now(tz=self.TZ) # When no speedup, now is correct
        return self.last_speedtime

    def get_speedup_val(self):
        return self.speedup_val

    def set_speedup_val(self, val):
        self.speedup_val = val


# If called directly
# Also used to develop/debug this module
if __name__ == '__main__' :
    speedup = 10
    t_fmt = '%Y/%m/%d %H:%M:%S'
    d_sp = speedup_date(enable_speedup = True, speedup_val = speedup)
    print("Using speedup ", speedup)
    while True:
        print(datetime.now(tz=self.TZ).strftime(t_fmt), '\t',d_sp.now(tz=self.TZ).strftime(t_fmt))
        sleep(1)

