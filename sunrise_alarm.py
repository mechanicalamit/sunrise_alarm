
# Python standard modules
from transitions import Machine
from datetime import datetime
import pytz

# Local modules
from sa_lib.rgb_profile import *

"""
State Machine for each alarm
"""
class RPiSunrise(object):

    states = ['START', 'IDLE', 'READY', 'RUN']

    def __init__(self, name, al, dis, d_sp):
        self.name = name
        self.al = al

        self.machine = Machine(model=self, states=RPiSunrise.states, initial='START',
                       after_state_change='after_state')

        self.machine.add_transition(trigger='init', source='START', dest='IDLE')
        self.machine.add_transition(trigger='activate', source='IDLE', dest='READY')
        self.machine.add_transition(trigger='snooze', source=['READY', 'RUN'], dest='IDLE')
        self.machine.add_transition(trigger='ring', source='READY', dest='RUN')

        self.profile = eval(al['profile'])() # This is an instantiation
        self.dis = dis
        self.d_sp = d_sp

    def get_al(self):
        return self.al

    # From datetime, return any alarm this is ready, otherwise return None
    # Repeat and counter not implemented yet.
    def is_ready(self, indate):
        hhmm = indate.hour * 100 + indate.minute
        if self.al['enabled'] and self.al['ready_dow'][indate.weekday()] and ( 0 <= (hhmm - self.al['ready_t']) < 2 ):
            return True
        return False

    def can_ring(self, indate):
        hhmm = indate.hour * 100 + indate.minute
        if self.al['enabled'] and self.al['run_dow'][indate.weekday()] and ( 0 <= (hhmm - self.al['run_t']) < 2 ):
            self.ringingal = al
            return True
        return False

    def set_start_ringing_time(self, indate):
        self.start_ringing_time = indate

    def is_done_ringing(self, indate):
        if self.get_cur_rgb(indate) is None:
            return True
        return False

    def get_ring_profile(self):
        return self.profile # returns instance of profile

    def get_cur_rgb(self, indate):
        seconds_elapsed = (indate-self.start_ringing_time).total_seconds()
        return self.profile.get_rgb(seconds_elapsed)

    def after_state(self):
        self.dis.add_t(self.al, self.state, self.d_sp.get_last_speed_stamp())
        self.dis.update_screen()

    def got_button(self):
        if self.state == 'RUN':
            self.snooze()
            return True
        if self.state == 'READY':
            self.snooze()
            return True
        return False


def got_button(Al_Machs):
    # Go over all alarms in reversed order, and tell them we got button
    # If they are able to do any action, then return True and bug out, else continue on next one
    for a in reversed(Al_Machs):
        if a.got_button():
            lghtsnd.blink_green_twice()
            return
    # No Machine could take action on button, all are idle
    print("Got Button : All IDLE")
    lghtsnd.blink_red_twice()

"""==== Instantiations =============================="""
# Global settings
import settings

# Instantiate display here
from sa_lib import display_prettytable
dis = display_prettytable.display()

# Speedup for testing here
from sa_lib import datetime_speedup
d_sp = datetime_speedup.speedup_date(TZ = settings.TZ, enable_speedup = settings.enable_speedup, speedup_val = settings.speedup)

# Light/Sound Hardware driver
from sa_lib.hardware_driver import Light_Sound
lghtsnd = Light_Sound(enable_hw = settings.enable_hw, enable_pyqt=settings.enable_pyqt, printer=dis)

#  Alarms from tsv file
from sa_lib.alarmdb import AlarmsDB
al_db = AlarmsDB(settings.al_db_file)

# Instantiate the state machine(s), one for each alarm
Al_State_Machs = []
for al in al_db.get_alarmdb():
    if al['enabled']:
        Al_State_Machs.append(RPiSunrise(str(al['alarm_no']), al, dis, d_sp))

# Button on RPi, 7 is the button
if settings.enable_hw:
    import RPi.GPIO as GPIO
    but_pin = 7
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(but_pin, GPIO.IN)

"""==== Start running here =========================="""

# Lets get the display rolling
dis.add_t(None, 'BEGIN', datetime.now(tz = pytz.timezone(settings.TZ)))
dis.update_screen()

""" Prestart """
for a in Al_State_Machs:
    a.init()
    a.activate()

"""
Scheduler
"""
while True:
    for a in Al_State_Machs:
        nw  = d_sp.now()
        al_no = a.get_al()['alarm_no']

        if a.state == 'START' :
            a.init()

        if a.state == 'IDLE' :
            if a.is_ready(nw):
                a.activate()

        if a.state == 'READY' :
            if a.can_ring(nw):
                a.set_start_ringing_time(nw)
                a.ring()

        if a.state == 'RUN' :
            d_sp.set_speedup_val(100) # Alarm is running, lets slow it down to see it better
            if a.is_done_ringing(nw):
                a.snooze()

    # Loop over all state machines,
    for a in Al_State_Machs:
        # If any machine state is RUN, set light/sound and break, else all off
        Machs_Running = [a for a in Al_State_Machs if a.state=='RUN']
        if Machs_Running:
            a_run = Machs_Running[0] # Take the first one (Priority is to lower number)
            rgbvals = a_run.get_cur_rgb(nw)
            lghtsnd.set_rgb(rgbvals)
            break
        else:
            d_sp.set_speedup_val(settings.speedup) # Alarm is done, speed it back up
            lghtsnd.alloff()

    # Check for button input
    if settings.enable_hw:
        but_inp = GPIO.input(but_pin)
        if not but_inp:  # Button is low active
            got_button(Al_State_Machs)

    # Wait and button press loop
    from sa_lib.bot_tools import wait
    ret_ch = wait(0.2,0.02)
    if ret_ch == 'b': # button simulator
            got_button(Al_State_Machs)
    if ret_ch == 'q':
        break
