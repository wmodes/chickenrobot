# light.py - sunrise/sunset class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import datetime
from suntime import Sun, SunTimeException
from datetime import datetime, timedelta
from dateutil import tz
from settings import *
import logging

# Auto-detect timezones
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

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
        logging.debug("Light:Now:" + now.strftime(TIME_FORMAT))
        logging.debug("Light:Sunrise:" + sr.strftime(TIME_FORMAT))
        logging.debug("Light:Open door:" + od.strftime(TIME_FORMAT))
        logging.debug("Light:Sunset:" + ss.strftime(TIME_FORMAT))
        logging.debug("Light:Close door:" + cd.strftime(TIME_FORMAT))
        if self.is_dark(dt):
            text = f"It is dark now in {self.location}. "
        else:
            text = f"It is daylight now in {self.location}. "
        # sunrise hasn't happened yet
        if now < sr:
            text += f"The sun will rise at {sr.strftime(TIME_FORMAT)}"
            if sr == od:
                 text += " and it should be light enough to open the doors. "
            else:
                text += f" and it will be light enough to open the doors at {od.strftime(TIME_FORMAT)}. "
        # sunset has not yet happened
        elif now < ss:
            text += f"The sun rose at {sr.strftime(TIME_FORMAT)} and will set at {ss.strftime(TIME_FORMAT)}"
            if ss == cd:
                 text += " and it should be dark enough to close the doors. "
            else:
                text += f" and it will be dark enough to close the doors at {cd.strftime(TIME_FORMAT)}. "
        # sunset already happened
        else:
            text += f"The sun set at {ss.strftime(TIME_FORMAT)}"
            if ss == cd:
                 text += " and it should be dark enough to close the doors. "
            elif now < cd:
                text += f" and it will be dark enough to close the doors at {cd.strftime(TIME_FORMAT)}. "
            else:
                text += f" and it was dark enough to close the doors at {cd.strftime(TIME_FORMAT)}. "
            tomorrow = datetime.now().astimezone(to_zone) +             timedelta(1)
            srt = self.sunrise(tomorrow)
            text += f"Tomorrow's sunrise is at {srt.strftime(TIME_FORMAT)}. "
        logging.info("Report:" + text)
        return text


def main():
    import sys
    logging.basicConfig(
        filename=sys.stderr,
        encoding='utf-8',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logger = logging.getLogger()

    # Felton, CA 37.0513° N, 122.0733° W
    city_name = "Felton, CA"
    latitude = 37.0513
    longitude = -122.0733
    sunrise_delay = 0 # minutes
    sunset_delay = 60 # minutes

    light = Light(city_name, latitude, longitude, sunrise_delay, sunset_delay)
    # now = datetime.now().astimezone(to_zone) + timedelta(hours=10)
    logging.info(light.report())

if __name__ == '__main__':
    main()
