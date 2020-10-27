import datetime
from suntime import Sun, SunTimeException
from datetime import datetime
from dateutil import tz

# Auto-detect timezones
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

# Felton, CA 37.0513° N, 122.0733° W
city_name = "Felton, CA"
latitude = 37.0513
longitude = -122.0733

sun = Sun(latitude, longitude)

# Get today's sunrise and sunset in UTC
today_sr_utc = sun.get_sunrise_time()
today_sr_local = today_sr_utc.astimezone(to_zone)
today_ss_utc = sun.get_sunset_time()
today_ss_local = today_ss_utc.astimezone(to_zone)

print('Today at {} the sun rose at {} and goes down at {} UTC'.
      format(city_name, today_sr_utc.strftime('%H:%M'), today_ss_utc.strftime('%H:%M')))
print('Today at {} the sun rose at {} and goes down at {} localtime'.
    format(city_name, today_sr_local.strftime('%H:%M'), today_ss_local.strftime('%H:%M')))
