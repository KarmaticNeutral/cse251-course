"""
------------------------------------------------------------------------------
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Tim Taylor

Purpose: Retrieve Star Wars details from a website

Instructions:

- Review instructions in I-Learn for this assignment.

The call to TOP_API_URL will return the following Dictionary.  Do NOT have this
dictionary hard coded - use the API call to get this dictionary.  Then you can
use this dictionary to make other API calls for data.

{
   "people": "http://swapi.dev/api/people/", 
   "planets": "http://swapi.dev/api/planets/", 
   "films": "http://swapi.dev/api/films/",
   "species": "http://swapi.dev/api/species/", 
   "vehicles": "http://swapi.dev/api/vehicles/", 
   "starships": "http://swapi.dev/api/starships/"
}

------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

# Const Values
TOP_API_URL = r'https://swapi.dev/api'

# Global Variables
call_count = 0

# TODO Add your threaded class definition here
class API_Call(threading.Thread):
    def __init__(self, URL, requestTitle):
        threading.Thread.__init__(self)
        self.URL = URL
        self.requestTitle = requestTitle

    def run(self):
        response = requests.get(self.URL)

        if response.status_code == 200:
            self.data = response.json()
        else:
            print("Error Executing " + self.requestTitle + " Request")

# TODO Add any functions you need here
class ReturnData:
    def __init__(self, count, dataStr):
        self.count = count
        self.dataStr = dataStr

def getItemName(item):
    return item['name']

def makeGetCalls(items):
    global call_count
    item_threads = []
    item_string = ""
    item_data = []

    for i in items:
        call = API_Call(i, str(i) + "Request")
        call_count += 1
        call.start()
        item_threads.append(call)

    for t in item_threads:
        t.join()
        item_data.append(t.data)

    item_data.sort(key=getItemName)

    for i in item_data[:-1]:
        item_string = item_string + i['name'] + ", "
    item_string = item_string + item_data[-1]['name']

    return ReturnData(len(item_data), item_string)

def main():
    global call_count
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from swapi.dev')

    # TODO Retrieve Top API urls
    top = API_Call(TOP_API_URL, "Top API URL")
    top.start()
    call_count += 1
    top.join()

    # TODO Retrieve Details on film 6
    film6 = API_Call(top.data['films'] + '6', 'Film 6 Request')
    film6.start()
    call_count += 1
    film6.join()

    character_return = makeGetCalls(film6.data['characters'])
    planet_return = makeGetCalls(film6.data['planets'])
    starship_return = makeGetCalls(film6.data['starships'])
    vehicles_return = makeGetCalls(film6.data['vehicles'])
    species_return = makeGetCalls(film6.data['species'])

    # TODO Display results
    log.write("----------------------------------------")
    log.write("Title   : " + film6.data['title'])
    log.write("Director: " + film6.data['director'])
    log.write("Producer: " + film6.data['producer'])
    log.write("Released: " + film6.data['release_date'])
    log.write("Characters: " + str(character_return.count))
    log.write(character_return.dataStr)
    log.write()
    log.write("Planets: " + str(planet_return.count))
    log.write(planet_return.dataStr)
    log.write()
    log.write("Starships: " + str(starship_return.count))
    log.write(starship_return.dataStr)
    log.write()
    log.write("Vehicles: " + str(vehicles_return.count))
    log.write(vehicles_return.dataStr)
    log.write()
    log.write("Species: " + str(species_return.count))
    log.write(species_return.dataStr)
    log.write()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()
