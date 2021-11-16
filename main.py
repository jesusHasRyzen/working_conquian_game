import base64

from random import random


import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import json
from base64 import decodebytes
from PIL import Image
from io import BytesIO
# in the form of a string which will be added to the given url
# used to look up quite honestly anything on wikipedia
main = Flask(__name__)


uname = ""
images = ""



@main.route('/')
def instructions():
    return render_template('index.html')




@main.route('/loggedIN', methods = ['post'])
def instructions2():
    pws = request.form["psw"]
    urlEncrypt = 'https://realpython-example-app2.herokuapp.com/?username='+pws
    # returnFromRequest = requests.get(urlEncrypt)
    # encryptPW = decode_to_string(returnFromRequest)
    pws = requests.get(urlEncrypt).content
    uname = request.form["uname"]


    urlRules = 'https://team-anything-microservice.herokuapp.com/get_rules'
    jsonresponse = requests.get(urlRules).json()
    rules = jsonresponse['deal']
    objective = jsonresponse['objective']
    pack = jsonresponse['pack']
    rank =  jsonresponse['rank']
    score = jsonresponse['score']
    link = jsonresponse['youtube']
    urlImages = 'https://team-anything-microservice.herokuapp.com/get_images'
    # images = requests.get(urlImages).json()
    # byte_array = bytes(images)
    # images_decoded = base64.decodebytes(byte_array)
    # images_decoded = BytesIO(images_decoded)

    return render_template("loggedIn.html", name = uname, rules = rules, objective = objective, pack = pack , rank = rank, score = score, link = link, pws = pws)

# @main.route('/getImages')
# def instructions3():
#     urlImages = 'https://team-anything-microservice.herokuapp.com/get_images'
#
#     # returnFromRequest = requests.get(urlEncrypt)
#     # encryptPW = decode_to_string(returnFromRequest)
#     return requests.get(urlImages).content

# class for settings in place to initiate the game
# such as knowing how many players and cards to deal
class Settings(object):
    def __init__(self, numOfPlayers, numOfCards):
        self.numberOfPlayers = numOfPlayers
        self.numberOfCards = numOfCards


# class Game(object):
#     def __init__(self, Deck, Settings):


# class for cards created via the deck Class
# current functions include creating new deck
# shuffle deck and print the deck
Suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
Values = ["Ace", 2, 3, 4, 5, 6, 7, "Jack", "Queen", "King"]
class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def printCard(self):
        print("{} of {}".format(self.value, self.suit))
class Deck(object):
    def __init__(self):
        self.cards = []
        self.newDeck()
        self.shuffleDeck()

    def newDeck(self):
        for suit in Suits:
            for val in Values:
                self.cards.append(Card(val, suit))

    def shuffleDeck(self):
        numOfCards = 40
        for i in range(numOfCards):
            j = int(random() * i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]


    def printDeck(self):
        for card in self.cards:
            card.printCard()

# class for the player where it initiates the player already having his
# hand and the options the player has such as switching cards to start
# the game, draw card, playcard and discard card
class Player(object):
    def __init__(self):
        self.hand = []
    # def switchCard(self):
    #
    # def drawACard(self, deck):
    # if needed :
    #     putDownSequence()
    # else:
    #     discardCard()
    # def passOnCard(self):
    #
    # def pickUpCard(self):
    #     playCardPickedUp()
    #
    # def discardCard(self):
    #
    # def playCardPickedUp(self):
    #     putDownSequence()
    #     discardCard()
    #
    # def putDownSequence(self):








myDeck = Deck()
myDeck.printDeck()
if __name__ == '__main__':
    # webSite.debug = True
    main.run()