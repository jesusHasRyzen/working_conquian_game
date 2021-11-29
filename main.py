import base64
import os

from random import random


import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

from os import system, name




import json
from base64 import decodebytes
from PIL import Image
from io import BytesIO

# in the form of a string which will be added to the given url
# used to look up quite honestly anything on wikipedia
main = Flask(__name__)


uname = ""
images = ""

def clear():
    os.system('clear')

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
# such as knowing how many players and cards to deal, sound on or off
# as well as adding the difficulty level
class Settings(object):
    def __init__(self, numOfPlayers, numOfCards, sound, difficulty):
        self.settingNumberOfPlayers = numOfPlayers
        self.settingNumberOfCards = numOfCards
        self.settingSound = sound
        self.settingDifficulty = difficulty

# functions to get the number of players, number of cards , sound on or off,
    # and difficulty in other classes or out of the scope of this class

    def getNumberOfPlayers(self):
        return self.settingNumberOfPlayers

    def getNumberOfCards(self):
        return self.settingNumberOfCards

    def getSound(self):
        return self.settingSound

    def getDifficulty(self):
        return self.settingDifficulty

# class for initiating the game, with the settings being taken into account.
# initiated the game with function startGame
class Table(object):
    cardsOnTable = dict()
    def __init__(self, numOfPlayers, numOfCards):
        self.numOfPlayerSlots = numOfPlayers
        self.numOfCards = numOfCards
        # self.setTable(self.numOfPlayerSlots, self.numOfCards)
    # def setTable(self, numOfSeats, numOfCards):
        # for seats in range(numOfSeats):
          # self.cardsOnTable[seats] = dict()       might not need it
          # print("player {} table cards".format(seats+1))
    # def addCardsToTable(self, player):

    def ViewTable(self, players, numberOfplayers):
        # for seats in range(self.numOfPlayerSlots):
        clear()
        amountIntent = 50 * numberOfplayers
        print("{:^{}}".format("Table 1", amountIntent))
        self.printPlayerSlots(numberOfplayers)
        for player in range(numberOfplayers):
            # print("{:^50}".format("player {} table cards".format(player + 1)), end="")
            # print
            players[player].printPlayedCards()
        for i in range(10):
            print("")
    def printPlayerSlots(self, numberOfSlots):
        amountIntent = 30
        for i in range(numberOfSlots):
            amountIntent = amountIntent + (amountIntent*i)
            # print("{:^{}}".format("player {} table cards".format(i + 1, amountIntent+(amountIntent*i))), end="")
            print("{:^{}}".format("player {} table cards".format(i + 1), amountIntent), end="")

class Game(object):
    isGameWon = False
    isGameTied =False
    CardsSwitched = []

    def __init__(self, Settings):
        self.numberOfPlayers = Settings.getNumberOfPlayers()
        self.numberOfCards = Settings.getNumberOfCards()
        self.sound = Settings.getSound()
        self.difficulty = Settings.getDifficulty()
        self.players = [Player(self.numberOfCards) for i in range(self.numberOfPlayers)]

        self.startGame()

# function starts the game with a new deck, and deals the cards to the players.
    def startGame(self):
        self.gameTable = Table(self.numberOfPlayers, self.numberOfCards)
        self.gameDeck = Deck()
        Deck.dealCards(self.gameDeck, self.players, self.numberOfPlayers)
        self.playersSwitchCards()
        # insert first draw here
        discardCount = self.numberOfPlayers
        cardDiscarded = Card
        clear()
        while not(self.isGameWon or self.isGameTied):
            # start with first player being able to pick up the first card or discarding
            # then loop for second and so on players
            for i in range(self.numberOfPlayers):
                print("player {} Hand".format(i + 1))
                if discardCount == self.numberOfPlayers:
                    cardDiscarded = self.players[i].drawACard(self.gameDeck)
                    discardCount = 1
                    self.gameTable.ViewTable(self.players, self.numberOfPlayers)

                    if self.players[i].hasWon():
                        break
                    continue
                if self.players[i].pickUpCardOrNot(cardDiscarded):
                    print("player {} Hand".format(i + 1))
                    cardsToPlay = self.players[i].selectCardsToPlay()
                    if self.players[i].isPlayable(cardsToPlay):
                        self.players[i].playCards(cardsToPlay)
                        cardDiscarded = self.players[i].discardCardAt()
                        self.gameTable.ViewTable(self.players[i], i)
                        if self.players[i].hasWon():
                            break
                else:
                    print("player {} Hand".format(i + 1))
                    discardCount = discardCount + 1
                    if discardCount == self.numberOfPlayers:
                        cardDiscarded = self.players[i].drawACard(self.gameDeck)
                        discardCount = 1
                        self.gameTable.ViewTable(self.players[i], i)
                        if self.players[i].hasWon():
                            break
                        continue
    def playersSwitchCards(self):
        self.playersSwitchCardsOut()
        self.playersSwitchCardsIn()
    def playersSwitchCardsOut(self):
        for i in range(self.numberOfPlayers):
            self.CardsSwitched.append(self.players[i].switchCardOut())
    def playersSwitchCardsIn(self):
        for i in range(self.numberOfPlayers):
            j = i + 1
            if(j == self.numberOfPlayers):
                j = 0
            self.players[j].switchCardIn(self.CardsSwitched[i])
    # def checkIfPlayerHasWon(self):

# function to print the hands held by all the players, its debugging mechanism to help see where each card went
    def printHands(self):
        for i in range(self.numberOfPlayers):
            print(f"player {i} has")
            # for count in range(self.numberOfCards):
            # print(f"{self.players[i].printHand()}")
            self.players[i].printHand()


# class for cards created via the deck Class
# current functions include creating new deck
# shuffle deck and print the deck
Suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
Values = {"Ace":0, "2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "Jack":7, "Queen":8, "King":9}

class Card(object):
    value = ""
    suit = ""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def printCard(self):
        print("{} of {}".format(self.value, self.suit))
# class for the deck to be created. it initiates the deck and then shuffles it.
# has a function to deal the top card of the deck to the next player and returns that card
# has function to deal cards to players
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
# function to deal the card on top of the deck
    def dealTopCard(self):
        cardsLeftCount = len(self.cards)
        cardToreturn = self.cards[cardsLeftCount-1]
        self.cards.pop(cardsLeftCount-1)
        return cardToreturn
# function to deal all cards to initiate the game
    def dealCards(self, players, numberOfPlayers):
            for i in range(numberOfPlayers):
                players[i].getHand(self)

# printing function for debugging

    def printDeck(self):
        for card in self.cards:
            card.printCard()

# class for the player where it initiates the player already having his
# hand and the options the player has such as switching cards to start
# the game, draw card, playcard and discard card
class Player(object):
    def __init__(self, cardCount):
        self.hand = []
        self.NumberCards = cardCount
        self.playedCards = []

    def pickUpCardOrNot(self, card):
        self.hand.append(card)
        self.printHand()
        playOrDiscardOption = int(input("Do you want to play (1) or Discard this card(0) :"))
        if playOrDiscardOption:
            return True
        else:
            self.discardCard()
            return False

    def getHand(self, deck):
        for i in range(self.NumberCards):
            self.hand.append(deck.dealTopCard())
    def returnCardAtPosition(self, position):
        return self.hand[position]
    def printPlayedCards(self):
        for card in self.playedCards:
            card.printCard()
    def printHand(self):
        # print(f"{self.hand[count]}")
        for card in self.hand:
            card.printCard()
    def switchCardOut(self):
        clear()
        self.printHand()
        positionToSwitch = input("enter position of card to Switch with Next Player:")
        positionToSwitch = int(positionToSwitch)
        positionToSwitch = positionToSwitch -1
        switchCard = self.hand[positionToSwitch]

        self.hand.pop(positionToSwitch)
        return switchCard
    def switchCardIn(self, card):
        self.hand.append(card)
    def drawACard(self, deck):
        cardDrawn = deck.dealTopCard()
        self.hand.append(cardDrawn)
        self.printHand()
        playerChoice = input("Do you wish to play card enter 1 or discard enter 0")
        playerChoice = int(playerChoice)
        if playerChoice:
            cardsToPlay = self.selectCardsToPlay()
            if self.isPlayable(cardsToPlay):
            # for testing purposes
                self.playCards(cardsToPlay)
# this section of the code is repeated in playCards function
                # for card in cardsToPlay:
                #     if card in self.hand:
                #         self.hand.remove(card)
                return self.discardCardAt()
        else:
             return self.discardCard()

    def discardCardAt(self):
        self.printHand()
        positionOfCard2Discard = int(input("select position of Card to discard"))
        card2Discard = self.hand[positionOfCard2Discard-1]
        self.hand.pop(positionOfCard2Discard-1)
        return card2Discard
    def discardCard(self):
        card2Discard = self.hand[len(self.hand)-1]
        self.hand.pop(len(self.hand)-1)
        return card2Discard
    def playCards(self, cards2Play):
        for card in cards2Play:
            self.playedCards.append(card)
            card.printCard()
            if card in self.hand:
                self.hand.remove(card)


    def selectCardsToPlay(self):
        finishSelecting = False
        cardsSelected = []
        while (finishSelecting == False):
            self.printHand()
            positionSelected = int(input("enter position of card to play or 9 when finished"))
            if positionSelected == 9:
                cardsSelected.append(self.returnCardAtPosition(len(self.hand)-1))
                finishSelecting = True
            else:
                cardsSelected.append(self.returnCardAtPosition(positionSelected-1))
        return cardsSelected
    # def putDownSequence(self):
    def isPlayable(self, Cards2Play):
        if self.isSequencial(Cards2Play):
            return True
        if self.arePairs(Cards2Play):
            return True
        else:
            return False
    def isSequencial(self, Cards2Play):
        values = []
        suits = []
        intVal = []
        for cards in Cards2Play:
            values.append(cards.value)
            suits.append(cards.suit)
        firstSuit = suits[0]
        for suit in suits:
            if firstSuit != suit:
                return False
        for val in values:
            intVal.append(Values.setdefault(val))

        values = sorted(intVal)

        for i in range(len(Cards2Play)-1):
            compareVal = int(values[i])
            tempFirst = int(values[i]) + 1
            tempSecond = int(values[i+1])
            if int(values[i])+1 == int(values[i+1]):
                continue
            else:
                return False
        return True

    def arePairs(self, Cards2Play):
        values = []
        suits = []
        for cards in Cards2Play:
            values.append(cards.value)
            suits.append(cards.suit)
        firstValue = values[0]
        for value in values:
            if firstValue != value:
                return False
        return True
    def hasWon(self):
        if not self.hand:
            return True
        else:
            return False


gameSettings = Settings(2, 8, "on", "easy")
startGame = Game(gameSettings)
startGame.printHands()

startGame.gameDeck.printDeck()


if __name__ == '__main__':
    # webSite.debug = True
    main.run()

