import csv
import os
import sys

"""
Alarm DataBase
"""
class AlarmsDB(object):


    def __init__(self, aldbfile):
        self.alarmdb = []
        self.rawtext = []

        with open(os.path.join(sys.path[0], aldbfile)) as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"):
                if line[0][0] != '#' :
                    self.add_alarm(line)
                    self.rawtext.append('\t'.join(line))
        self.process_raw_alarmdb()

    def add_alarm(self, al_tup):
        self.alarmdb.append ( {'alarm_no': al_tup[0], 'enabled' : al_tup[1], 'dow' : al_tup[2],
            'ready_t' : al_tup[3], 'run_t' : al_tup[4], 'repeat': al_tup[5], 'counter' : al_tup[6], 'profile' : al_tup[7] } )

    def parsedow(self, instr):
        t_li = [False] * 7 # Monday = index 0, Tuesday = index 1, ...
        instr.replace(" ", "") # remove spaces
        instr = instr.split(",") # Make fields/tokens in place

        # Lets deal with each one by one, all single digits with or without a dash in the middle
        for fi in instr:
            if len(fi) == 1:
                t_li[int(fi) % 7] = True
            if len(fi) == 3:
                for i in range(int(fi[0]), int(fi[2])+1):
                        t_li[int(i) % 7] = True

        return t_li

    def process_raw_alarmdb(self):

        validYN = {"yes": True, "y": True, "ye": True, "no": False, "n": False}

        for al in self.alarmdb:
            al['alarm_no'] = int(al['alarm_no'])
            al['enabled'] = validYN[al['enabled'].lower()]
            al['dow'] = self.parsedow(al['dow'])
            al['run_t'] = int(al['run_t'])
            al['ready_t'] = int(al['ready_t'])
            al['repeat'] = validYN[al['repeat'].lower()]
            al['counter'] = int(al['counter'])
            al['profile'] = str(al['profile']) # Lets keep it as a string

            # If ready_t is > run_t : it falls on the previous day. DOW for ready_t then has to be fixed for days before
            if al['ready_t'] > al['run_t']:
                al['ready_dow'] = al['dow'][1:] + [al['dow'][0]]
            else:
                al['ready_dow'] = al['dow']

    def print_alarmdb(self):
        import pprint
        pprint.pprint(self.alarmdb)

    def get_no_alarms(self):
        return len(self.alarmdb)

    def get_alarmdb(self):
        return self.alarmdb

    def get_rawtext(self):
        return self.rawtext

