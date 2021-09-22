"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')   # Do not change the path.
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
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

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52

    def reshuffle(self):
        res = Request_thread(f'http://deckofcardsapi.com/api/deck/{deck_id}/shuffle/', "Reshuffle Your Deck")
        res.start()
        res.join()
        self.remaining = res.data['remaining']
        return res.data['success']

    def draw_card(self, num_cards=1):
        card = Request_thread(f'http://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={num_cards}', "Draw a Card Thread")
        card.start()
        card.join()
        self.remaining = card.data['remaining']
        return card.data

    def cards_remaining(self):
        return self.remaining

    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'q2h9j1v8ga55'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

