# chickenrobot - a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

from light import Light
from door import Door

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

    def report(self):
        return self.light.report() + "\n" +
            self.door.report()


def main():
    # nuthin here yet
    chickenrobot = Chickenrobot()
    print(chickenrobot.report())

if __name__ == '__main__':
    main()
