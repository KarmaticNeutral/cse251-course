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
import multiprocessing as mp

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

def makeCall(url):
    call = API_Call(url, f'API Request on {url}')
    call.start()
    call.join()
    return call.data['name']

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

    characterList = []
    planetList = []
    starshipList = []
    vehicleList = []
    speciesList = []

    character_pool = mp.Pool(6)
    planet_pool = mp.Pool(5)
    starship_pool = mp.Pool(5)
    vehicle_pool = mp.Pool(5)
    species_pool = mp.Pool(5)

    for char in film6.data['characters']:
        call_count += 1
        character_pool.apply_async(makeCall, args=(char, ), callback=characterList.append)
    for planet in film6.data['planets']:
        call_count += 1
        planet_pool.apply_async(makeCall, args=(planet, ), callback=planetList.append)
    for starship in film6.data['starships']:
        call_count += 1
        starship_pool.apply_async(makeCall, args=(starship, ), callback=starshipList.append)
    for vehicle in film6.data['vehicles']:
        call_count += 1
        vehicle_pool.apply_async(makeCall, args=(vehicle, ), callback=vehicleList.append)
    for species in film6.data['species']:
        call_count += 1
        species_pool.apply_async(makeCall, args=(species, ), callback=speciesList.append)

    character_pool.close()
    planet_pool.close()
    starship_pool.close()
    vehicle_pool.close()
    species_pool.close()

    character_pool.join()
    planet_pool.join()
    starship_pool.join()
    vehicle_pool.join()
    species_pool.join()

    characterList.sort()
    planetList.sort()
    starshipList.sort()
    vehicleList.sort()
    speciesList.sort()
    
    # TODO Display results
    log.write("----------------------------------------")
    log.write("Title   : " + film6.data['title'])
    log.write("Director: " + film6.data['director'])
    log.write("Producer: " + film6.data['producer'])
    log.write("Released: " + film6.data['release_date'])
    log.write("Characters: " + str(len(characterList)))
    log.write(characterList)
    log.write()
    log.write("Planets: " + str(len(planetList)))
    log.write(planetList)
    log.write()
    log.write("Starships: " + str(len(starshipList)))
    log.write(starshipList)
    log.write()
    log.write("Vehicles: " + str(len(vehicleList)))
    log.write(vehicleList)
    log.write()
    log.write("Species: " + str(len(speciesList)))
    log.write(speciesList)
    log.write()

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')
    

if __name__ == "__main__":
    main()
