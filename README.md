
A very flexible RGB Alarm Clock written in Python3 using the transitions state machine.

Initially written for simulating a sunrise on a Raspberry Pi for a natural waking, 
the project has expanded into a very flexible state machine based alarm system 
with some nice features
- Unlimited RGB Alarms with day-of-week and repeat settings
- Customizable RGB profiles associated with each alarm. E.g. Sunrise, blink. Or write your own
- Pre-Cancel alarm previous night for one time only. E.g Want to sleep in for one day
- Speedup module for testing alarms and developing RGB profiles
- Each alarm is independently run with its own state machine

### Hardware Setup

Pinout  
Red Led = Pin 22  
Green Led = Pin 18  
Blue Led = Pin 17  
Snooze Button = Pin 7 (Active Low)


### Software Setup

Python3 is used for this project.

The following modules are needed
- Transitions (for state machine, [github](https://github.com/tyarkoni/transitions.git))
- PyQt5 (for graphical output, optional)
- RPi.GPIO (for input button)
- pytz (for timezone)
- pprint (for text display)
- pi-blaster (for PWM of Pins)  
... and others


#### Steps to get software up and running
* Clone this repository
* Update alarms\_db.tsv. Details are within the file itself
* Use existing RGB profile or write your own profiles. (Sorry the profiles are
  a little complex. However, the profiles are very flexible and potential disco
  lights could be made)
* Run screen/tmux since the scripts dump text on screen showing alarm(s) state
* Run sunrise\_alarm.py (python3)


### Coming Sooner(or later), aka Roadmap:
- Sound capability
- RESTful API for web control
- Modify alarms from Android App (based on RESTful)
- Qt5 based RGB Alarm Profile maker. Build profiles visually instead of coding
