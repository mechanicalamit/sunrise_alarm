
"""
This class is the base class for rgb profile. Instances of this class
will be used to run rgb color profile over time.

Input : time delta in seconds (cannot be negative)
Output : rgb value (tuple)

"""
class RGB_Profile(object):
    totaltime = 40 # minutes
    total_seconds = totaltime * 60 # seconds

    def __init__(self):
        pass

    # get_rgb gets seconds_elapsed since alarm started ringing
    # get_rgb must return None when alarm has to stop
    # Input : seconds since alarm started ringing
    # Output : rgb value or None. White is (255,255,255)
    def get_rgb(self, seconds_elapsed):
        if seconds_elapsed > self.total_seconds:
            return None
        else:
            r_val = min(255, int(seconds_elapsed * 0.5))
            g_val = min(255, max(0, int(seconds_elapsed * 0.5 -500)))
            b_val = min(255, max(0, int(seconds_elapsed-1400)))
            return (r_val, g_val, b_val) 

    def get_totaltime(self):
        return self.totaltime

    def get_total_seconds(self):
        return self.total_seconds

"""==== User defined RGB Profiles =================================="""
# Other profiles that are inherited, in this case simple copies 
rgb_morning_dad = RGB_Profile

# Other profiles would be children of RGB_Profile
# Wanted to use super
class Nightlight(RGB_Profile):
    totaltime = 8 * 60 # minutes, 8 hours, all night
    total_seconds = totaltime * 60 # seconds

    def __init__(self):
        super().__init__()

    def get_rgb(self, seconds_elapsed):
        if seconds_elapsed > self.total_seconds:
            return None
        else:
            # Night is low white light
            col_level = 75
            return (col_level, col_level, col_level) 

# Blink full white, on/off every second
class Blink(RGB_Profile):
    totaltime = 30 # minutes, 8 hours, all night
    total_seconds = totaltime * 60 # seconds

    def __init__(self):
        super().__init__()

    def get_rgb(self, seconds_elapsed):
        if seconds_elapsed > self.total_seconds:
            return None
        else:
            col_level = int(seconds_elapsed % 2) * 255
            return (col_level, col_level, col_level) 

# Class to solve MRO issues
class Sunrise(RGB_Profile):
    pass

# Multiple Inheritence. Hurrah!!
# Totally unneccessary, but 
class rgb_morning_son(Sunrise, Blink):
    totaltime = Sunrise.totaltime + Blink.totaltime # minutes
    total_seconds = totaltime * 60 # seconds

    def __init__(self):
        super().__init__() # Pretty redundant in this case, but hey OOP

    # For the son, try a regular sunrise first, then move to the agressive blink after that
    def get_rgb(self, seconds_elapsed):
        if seconds_elapsed > self.total_seconds:
            return None
        else:
            if seconds_elapsed < Sunrise.total_seconds:
                return Sunrise.get_rgb(self, seconds_elapsed)
            else:
                return Blink.get_rgb(self, seconds_elapsed - Sunrise.total_seconds )


# If called directly
if __name__ == '__main__' :
    a = rgb_morning_son()

