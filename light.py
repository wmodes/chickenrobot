# light.py - sunrise/sunset class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import datetime
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta
from dateutil import tz

# Auto-detect timezones
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# DEBUG = True
DEBUG = False

class Light(object):
    """reports sunrise and sunset times"""
    def __init__(self, location, lat, long, sunrise_delay, sunset_delay):
        self.location = location
        self.lat = lat
        self.long = long
        self.sunrise_delay = sunrise_delay
        self.sunset_delay = sunset_delay
        self.sun = Sun(lat, long)
    def sunrise(self, dt=None):
        """returns today's sunrise in local time"""
        return self.sun.get_local_sunrise_time(dt)
    def open_door(self, dt=None):
        """returns today's sunrise in local time + sunrise_delay """
        return self.sunrise(dt) + timedelta(minutes=self.sunrise_delay)
    def sunset(self, dt=None):
        """returns today's sunset in local time"""
        ss = self.sun.get_local_sunset_time(dt)
        sr = self.sun.get_local_sunrise_time(dt)
        if ss < sr:
            tomorrow = datetime.now().astimezone(to_zone) +             timedelta(1)
            ss = self.sun.get_local_sunset_time(tomorrow)
        return ss
    def close_door(self, dt=None):
        """returns today's sunset in local time + sunset_delay"""
        return self.sunset(dt) + timedelta(minutes=self.sunset_delay)
    def is_dark(self, dt=None):
        now = datetime.now().astimezone(to_zone)
        if dt: now = dt
        od = self.open_door(dt)
        cd = self.close_door(dt)
        if od < now < cd:
            return False
        return True
    def is_light(self, dt=None):
        return not self.is_dark(dt)
    def report(self, dt=None):
        """returns a report string"""
        sr = self.sunrise(dt)
        od = self.open_door(dt)
        ss = self.sunset(dt)
        cd = self.close_door(dt)
        now = datetime.now().astimezone(to_zone)
        if dt: now = dt
        if DEBUG: print("DEBUG: now", now)
        if DEBUG: print("DEBUG: sunrise", sr)
        if DEBUG: print("DEBUG: open door", od)
        if DEBUG: print("DEBUG: sunset", ss)
        if DEBUG: print("DEBUG: close door", cd)
        if self.is_dark(dt):
            text = f"Light status: It is dark now in {self.location}. Doors should be closed.\n"
        else:
            text = f"Light status: It is daylight now in {self.location}. Doors should be open.\n"
        # sunrise hasn't happened yet
        if now < sr:
            text += f"\tThe sun will rise at {sr.hour}:{sr.minute}"
            if sr == od:
                 text += " when the doors will open."
            else:
                text += f" and the doors will open at {od.hour}:{od.minute}."
            return text
        # sunset has not yet happened
        elif now < ss:
            text += f"\tThe sun will set at {ss.hour}:{ss.minute}"
            if ss == cd:
                 text += " when the doors will close."
            else:
                text += f" and the doors will close at {cd.hour}:{cd.minute}."
            return text
        # sunset already happened
        else:
            text += f" The sun set at {ss.hour}:{ss.minute}"
            if ss == cd:
                 text += " and the doors closed."
            else:
                text += f" and the doors closed at {cd.hour}:{cd.minute}."
            tomorrow = datetime.now().astimezone(to_zone) +             timedelta(1)
            srt = self.sunrise(tomorrow)
            text += f" Tomorrow's sunrise is at {srt.hour}:{srt.minute}."
            return text


def main():
    # Felton, CA 37.0513° N, 122.0733° W
    city_name = "Felton, CA"
    latitude = 37.0513
    longitude = -122.0733
    sunrise_delay = 0 # minutes
    sunset_delay = 60 # minutes

    light = Light(city_name, latitude, longitude, sunrise_delay, sunset_delay)
    # now = datetime.now().astimezone(to_zone) + timedelta(hours=10)
    print(light.report())

if __name__ == '__main__':
    main()
