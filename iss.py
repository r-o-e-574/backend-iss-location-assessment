#!/usr/bin/env python

__author__ = 'Ruben Espino with help from Chris Warren'

import requests
import turtle
import time

iss = 'isscustom.gif'
earth = 'map.gif'
public_api = 'http://api.open-notify.org'


def astronauts_on_board():
    """Obtain a list of astronauts that are currently in space.
    Print full names,
    spacecraft they are onboard,
    and total number of astronauts in space
    """
    r = requests.get(public_api + '/astros.json')
    r.raise_for_status()  # raises stored HTTPError if one occurred
    return r.json()['people']


def current_coordinates():
    """Obtain the current geo coordinates (lat/lon) of iss,
    along with timestamp
    """
    r = requests.get(public_api + '/iss-now.json')
    r.raise_for_status()  # raises stored HTTPError if one occurred
    time_stamp = r.json()['timestamp']
    time_stamp_readable = time.ctime(time_stamp)
    coords = r.json()['iss_position']
    lat = float(coords['latitude'])
    lon = float(coords['longitude'])
    return lat, lon, time_stamp_readable


def world_map():
    """Create a graphics screen with world map image and ISS icon on lat/lon"""
    world_map = turtle.Screen()
    world_map.setup(720, 360)
    world_map.bgpic(earth)
    world_map.setworldcoordinates(-180, -90, 180, 90)
    world_map.title('ISS Locator Live Feed')
    world_map.register_shape(iss)
    space_station = turtle.Turtle()
    space_station.shape(iss)
    space_station.setheading(90)
    plot_overhead()
    while True:
        # Current coordinates of ISS
        lat, lon, time_stamp_readable = current_coordinates()
        print('Current ISS coordinates: Lat = {} Lon = {} Timestamp = {}'
              .format(lat, lon, time_stamp_readable))
        space_station.penup()
        space_station.goto(lon, lat)  # lon and lat are reversed
        time.sleep(7)
    return world_map


def next_overhead_time(lat, lon):
    """Find out the next time the ISS will be overhead specified lat/lon"""
    paramaters = {'lat': lat, 'lon': lon}
    r = requests.get(public_api + '/iss-pass.json', params=paramaters)
    r.raise_for_status()   # raises stored HTTPError if one occurred
    overhead_time = r.json()['response'][1]['risetime']
    return time.ctime(overhead_time)


def plot_overhead():
    try:
        # Show the next time ISS will be overhead Indianapolis, IN
        indy_lat = 39.768403
        indy_lon = -86.158068
        location = turtle.Turtle()
        location.penup()
        location.color('yellow')
        location.goto(indy_lon, indy_lat)
        location.dot()
        location.hideturtle()
        next_time_overhead = next_overhead_time(indy_lat, indy_lon)
        city_name = ' Indianapolis, IN'
        location.write(
            next_time_overhead + city_name,
            align='center',
            font=('Courier', 13, 'bold')
        )
    except RuntimeError as error:
        print('ERROR: problem loading graphics: ' + str(error))


def main():
    # Astronauts and their crafts
    astronauts_dict = astronauts_on_board()
    print('Current astronauts in space: {} \n'.format(len(astronauts_dict)))
    for i in astronauts_dict:
        print('Astronaut: {}\nSpacecraft: {}\n'.format(i['name'], i['craft']))
    # Create and display ISS on world map
    # world = None
    # Try to show turtle
    world_map()

    # if world is not None:
    # print('Click world map to exit')
    # world.exitonclick()


if __name__ == '__main__':
    main()
