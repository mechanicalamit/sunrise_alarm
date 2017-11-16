

from prettytable import PrettyTable
from datetime import datetime
import pytz
import platform
import os

#  Alarms from tsv file
import settings


class display(object):
    def __init__(self):
        self.x = PrettyTable()
        self.x._set_field_names([" Al.No ", " Wall Time ", " Stamp Time ", " State "])
        self.t_no  = 0

        self.ET_TZ = pytz.timezone('US/Eastern')

        from sa_lib.alarmdb import AlarmsDB
        al_db = AlarmsDB(settings.al_db_file)
        self.aldbrawtext = al_db.get_rawtext()

    def add_t(self, al, state, timestamp):
        #et_time = datetime.now(tz=self.ET_TZ).strftime("%Y/%m/%d %H:%M:%S")
        if al is None:
            al_no = 0
        else:
            al_no = al['alarm_no']
        et_time = datetime.now(tz=self.ET_TZ)

        t_fmt = '%Y/%m/%d %H:%M:%S'
        self.x.add_row([al_no, et_time.strftime(t_fmt), timestamp.strftime(t_fmt), state])
        self.t_no += 1

        if self.t_no > 15 :
            self.x.del_row(0)

    def print(self, rgbvals):
        print('\r                                              ', end="")
        print('\rCurrent RGB : ', rgbvals, end="")

    def update_screen(self):
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        print('No.\tEnabled\tDOW\tReady_T\tRun_T\tRepeat\tCounter\tProfile')
        for line in self.aldbrawtext:
            print(line)
        print(self.x)

