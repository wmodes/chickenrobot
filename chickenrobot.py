# chickenrobot - a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

from light import Light
from door import Door
from time import sleep

# constants
# Felton, CA 37.0513° N, 122.0733° W
city_name = "Felton, CA"
latitude = 37.0513
longitude = -122.0733
sunrise_delay = 0 # minutes
sunset_delay = 60 # minutes

revs = 10   # number of revolutions to bring door up or lower it down

# General psuedocode
#
# Listen for text/email [comms]
# Respond to text/email [comms]
# 	Send photos [comms]
# 	Report status
# 	Open door
# 	Close door
# Check for sunrise / sunset triggers [chickenrobot]
# 	Sleep in between checks [chickenrobot]
# 	Close door [door]
# 	Open door [door]
# 	Send status [comms]
# 	Send photos [comms]
# Open door [door]
# Close door [door]
# Take photo [cam]
# Get sunrise / sunset times [light]

class Chickenrobot(object):
    """controller class for a coop door and cam controller"""
    def __init__(self):
        self.light = Light(city_name, latitude, longitude, sunrise_delay, sunset_delay)
        self.light.report()
        self.door = Door(revs)
        self.door.report()

    def on_duty(self):
        print("Chicken Robot: On duty.")
        while(1):
            if self.light.is_dark() and self.door.is_open():
                self.door.close_door()
                self.report()
            elif self.light.is_light() and self.door.is_closed():
                self.door.open_door()
                self.report()
            else:
                sleep(5)
                print('.')

    def report(self):
        print("Chicken Robot: On duty.")
        print(self.light.report())
        print(self.door.report())


def main():
    # nuthin here yet
    chickenrobot = Chickenrobot()
    print(1)
    print(chickenrobot.report())
    print(2)
    chickenrobot.on_duty()

if __name__ == '__main__':
    main()
