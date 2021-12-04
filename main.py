# Author Jesus Ponce
# Completed by 12/3/21
import os

from random import random
import csv

import requests
from getpass import getpass
from flask import Flask, render_template, request
from os import system, name
import json






# function that calls a microservice that will get all the rules with a video of how to play the game.
# This way, the microservice is only called once and store in a global variable that can be accessed
# anywhere.
def getRules():
    urlRules = 'https://team-anything-microservice.herokuapp.com/get_rules'
    jsonresponse = requests.get(urlRules).json()
    rules = jsonresponse['deal']
    objective = jsonresponse['objective']
    pack = jsonresponse['pack']
    rank = jsonresponse['rank']
    score = jsonresponse['score']
    link = jsonresponse['youtube']
    setOfRules = "Rules : {}\nObjective : {}\nPack : {}\nRank : {}\nScore : {}\nLink : {}".format(rules, objective,
                                                                                                  pack, rank, score,
                                                                                                  link)
    return setOfRules


# column names for the csv file that will be created to keep track of all the users and their wins, ties.
# essentially the database for the login page.
columnNames = ["username", "pw", "wins", "losses", "ties"]
#  rules of the game is a global variable in order to print the rules of the game anywhere in the program
rulesOfGame = getRules()
#  this variable is used to keep a temp copy of the users, in order to make changes in file whent the game
# such as adding the number of wins, ties etc
playersInfo = []
# variables for the card objects to be created to make up the deck
Suits = ["Clubs", "Spades", "Hearts", "Diamonds"]
Values = {"Ace":0, "2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "Jack":7, "Queen":8, "King":9}
# a clear function to clear out the console
def clear():
    os.system('clear')
# a clear function that also prints out the rules of the game, these were obtained via the microservice request
def clearwithRules():
    os.system('clear')
    print("Rules of the game are as follows")
    print(rulesOfGame)
    for i in range(4):
        print("")

# function here created the database for the login to keep track of all the users.
def dataBase():
    with open("ConquianUsers.csv", mode="w") as usersFile:
        usersFileWriter = csv.DictWriter(usersFile, fieldnames=columnNames)




# class for settings in place to initiate the game
# such as knowing how many players and cards to deal, sound on or off
# as well as adding the difficulty level
# it also set up the game with the login page. allows the users to login
# or create a new account
class Settings(object):
    playerName = ""
    playersInfo = []
    def __init__(self, numOfPlayers, numOfCards, sound, difficulty):
        self.settingNumberOfPlayers = numOfPlayers
        self.settingNumberOfCards = numOfCards
        self.settingSound = sound
        self.settingDifficulty = difficulty
        self.startSetUp()
        self.canPlay = True

# functions to get the number of players, number of cards , sound on or off,
    # and difficulty in other classes or out of the scope of this class
    def startSetUp(self):
        self.Welcome()
        for i in range(self.settingNumberOfPlayers):
            # print("Player {} please login or create account".format(i+1))
            # if self.loginORcreate():
            #     self.userLogin()
            # else:
            #     self.createUser()
            print("Player {} please login".format(i + 1))
            print("Please enter 0 onto username to create account :")
            self.userLogin()
            clear()
            print("Welcome {}".format(self.playerName))


    def Welcome(self):
        print("Welcome To Conquian")

    # function that allows the users to login
    def userLogin(self):
        username = input("UserName:")
        if username == '0':
            print("Please Create account in order to play :")
            self.createUser()
        else:
            pw = getpass()
            pw = self.encryptPw(pw)
            verifyLogin = self.userExist(username, pw)
            if not verifyLogin:
                clear()
                print("Please enter matching Username and Password\nor enter 0 to create account: ")
                self.userLogin()
        return True

    # function to create an account
    def createUser(self):
        if self.verifyUsername():
            self.verifyPW()
            self.updateUsers()
            clear()
            self.userLogin()
        clear()
        print("Thanks for attempting to play")
        self.canPlay = False
    # function that will add users to database
    def updateUsers(self):
        with open("ConquianUsers.csv", mode="a") as usersFile:
            writer = csv.DictWriter(usersFile, fieldnames= columnNames)
            writer.writerow({"username": self.playerName, "pw": self.playerPw, "wins" : 0, "losses" : 0, "ties" : 0})
    # function will check if the user exists in the database already
    def userExist(self, user, pW):
        #if the user exist then return true else false
        with open("ConquianUsers.csv", mode='r') as usersFile:
            usersFileReader = csv.DictReader(usersFile, fieldnames= columnNames)
            for row in usersFileReader:
                if row["username"] == user:
                    pwFromCsv = row["pw"]
                    pW = str(pW)
                    if pwFromCsv == pW:
                        self.playerName = row["username"]
                        self.playersInfo.append(row)
                        return True
        return False


    # function to verify username, when creating new account.
    def verifyUsername(self):
        verification = False
        attempted = 0
        while not verification:
            if attempted:
                print("please enter matching username")
            print("if you wish to cancel enter 0")
            username = input("Username: must be only characters :").lower()
            if username == "0":
                break
            if self.isNameUsed(username):
                print("Username is used, choose a different name :")
                self.verifyUsername()
            usernameVerify = input("Verify Username: ").lower()
            if username == usernameVerify:
                self.playerName = username
                verification = True
                return verification
            attempted = attempted + 1
        return False
    # checks if the username is valid
    def isNameUsed(self, user):
        with open("ConquianUsers.csv", mode='r') as usersFile:
            usersFileReader = csv.DictReader(usersFile, fieldnames= columnNames)
            for row in usersFileReader:
                if row["username"] == user:
                    return True
        return False
    #  fucniton to verify the password, when creating new accoutn
    def verifyPW(self):
        verification = False
        attempted = 0
        while not verification:
            if attempted:
                print("please enter matching password")
            pw = getpass()
            pwVerify = getpass()
            if pw == pwVerify:
                self.playerPw = str(self.encryptPw(pw))
                verification = True
                print("Successfully Registered!!")
            attempted = attempted + 1
    # fucntion where microservice to encrypt the password is made and the encrypted password is returned
    def encryptPw(self, pws):
        # urlEncrypt = 'https://realpython-example-app2.herokuapp.com/?username='+pws
        urlEncrypt = 'https://cs361-encrypt-me.herokuapp.com/?username=' +pws
        pws = requests.get(urlEncrypt).content
        return pws

    def getNumberOfPlayers(self):
        return self.settingNumberOfPlayers
    def getNumberOfCards(self):
        return self.settingNumberOfCards
    def getPlayersInfo(self):
        return self.playersInfo
    def getSound(self):
        return self.settingSound
    def getDifficulty(self):
        return self.settingDifficulty

# class object that is a table. it is an object used to print out the cards on the table placed by the users.
class Table(object):
    cardsOnTable = dict()
    def __init__(self, numOfPlayers, numOfCards):
        self.numOfPlayerSlots = numOfPlayers
        self.numOfCards = numOfCards
    def ViewTable(self, players, numberOfplayers):
        clearwithRules()
        highestPlayedCards = 0
        numCardsPlayedByPlayer = []
        amountIntent = 50 * numberOfplayers
        print("{:^{}}".format("Table 1", amountIntent))
        self.printPlayerSlots(numberOfplayers)
        for player in range(numberOfplayers):
            self.cardsOnTable[player] = players[player].returnPlayedCards()
            numCardsPlayedByPlayer.append(len(self.cardsOnTable[player]))
            players[player].returnPlayedCards()
            i = player + 1
            if player == (numberOfplayers-1):
                break
        for i in range(len(numCardsPlayedByPlayer)):
            if numCardsPlayedByPlayer[i] > highestPlayedCards:
                highestPlayedCards = numCardsPlayedByPlayer[i]
        for i in range(highestPlayedCards):
            print("")
            for player in range(numberOfplayers):
                amountIntent = 50
                amountIntent = amountIntent + (amountIntent * player)
                if bool(self.cardsOnTable[player]):
                    if len(self.cardsOnTable[player]) < i+1:
                        continue
                    print("{:^{}}".format(self.cardsOnTable[player][i].getCard(), amountIntent), end="")
        for i in range(10):
            print("")
    # function to print out the location of the players slots on the table.
    def printPlayerSlots(self, numberOfSlots):
        amountIntent = 30
        for i in range(numberOfSlots):
            amountIntent = amountIntent + (amountIntent*i)
            print("{:^{}}".format("player {} table cards".format(i + 1), amountIntent), end="")
        print("")
# class for initiating the game, with the settings being taken into account.
# initiated the game with function startGame, the game is played in this object

class Game(object):
    isGameWon = False
    isGameTied =False
    CardsSwitched = []
    cardsLeft = 0
    playerWinner = 0

    def __init__(self, Settings):
        self.numberOfPlayers = Settings.getNumberOfPlayers()
        self.numberOfCards = Settings.getNumberOfCards()
        self.sound = Settings.getSound()
        self.difficulty = Settings.getDifficulty()
        self.players = [Player(self.numberOfCards) for i in range(self.numberOfPlayers)]
        self.playersInfo = Settings.getPlayersInfo()
        self.startGame()

# function starts the game with a new deck, and deals the cards to the players.
#     players then play the game of rummy following the rules placed under the
    #     global variable by that name. the game begin with the players switching
    # cards and then the first player draws the first card and decides whether to play
    # discard the card. this is played until the cards run out, there is a tie
    #  else one player is declared the winner by playing all their cards.

    def startGame(self):
        self.gameTable = Table(self.numberOfPlayers, self.numberOfCards)
        self.gameDeck = Deck()
        Deck.dealCards(self.gameDeck, self.players, self.numberOfPlayers)
        self.cardsLeft = 40 - self.numberOfPlayers * self.numberOfCards
        self.playersSwitchCards()
        # insert first draw here
        discardCount = self.numberOfPlayers
        cardDiscarded = Card
        clear()
        while not(self.isGameWon or self.isGameTied):
            # start with first player being able to pick up the first card or discarding
            # then loop for second and so on players
            for i in range(self.numberOfPlayers):

                print("{}'s Hand".format(self.playersInfo[i].get("username")))
                if discardCount == self.numberOfPlayers:
                    cardDiscarded = self.players[i].drawACard(self.gameDeck)
                    self.isGameWon = self.players[i].checkifWon()
                    if self.isGameWon:
                        # self.playerWinner = i + 1
                        break
                    if cardDiscarded == self.gameDeck.getEmptyCard():
                        self.isGameTied = True
                        break
                    self.cardsLeft = self.cardsLeft -1
                    discardCount = 1
                    self.gameTable.ViewTable(self.players, self.numberOfPlayers)

                    if self.players[i].hasWon():
                        break
                    continue
                if self.players[i].pickUpCardOrNot(cardDiscarded):
                    # if cardDiscarded == self.gameDeck.getEmptyCard():
                    #     self.isGameTied = True
                    #     break
                    print("{}'s Hand".format(self.playersInfo[i].get("username")))
                    cardsToPlay = self.players[i].selectCardsToPlay()
                    if self.players[i].isPlayable(cardsToPlay):
                        self.players[i].playCards(cardsToPlay)
                        self.isGameWon = self.players[i].checkifWon()
                        if self.isGameWon:
                            # self.playerWinner = i + 1
                            break
                        cardDiscarded = self.players[i].discardCardAt()
                        self.gameTable.ViewTable(self.players, self.numberOfPlayers)
                        if self.players[i].hasWon():
                            break
                else:
                    print("{}'s Hand".format(self.playersInfo[i].get("username")))
                    discardCount = discardCount + 1
                    if discardCount == self.numberOfPlayers:
                        cardDiscarded = self.players[i].drawACard(self.gameDeck)
                        self.isGameWon = self.players[i].checkifWon()
                        if self.isGameWon:
                            # self.playerWinner = i + 1
                            break
                        if cardDiscarded == self.gameDeck.getEmptyCard():
                            self.isGameTied = True
                            break
                        self.cardsLeft = self.cardsLeft - 1
                        discardCount = 1
                        self.gameTable.ViewTable(self.players, self.numberOfPlayers)
                        if self.players[i].hasWon():
                            break
                        continue
            if self.isGameWon:
                print("Game Winner is Player {}".format(self.playersInfo[i].get("username")))
                self.playersInfo[i]["wins"] = int(self.playersInfo[i].get("wins")) + 1

                # self.winnersNLoser()
                break
            if self.isGameTied:
                print("Game is tied no winner!!!!")
                for player in self.playersInfo:
                    player["ties"] = int(player.get("ties")) + 1
                break
        self.updateUsersInfo(self.playersInfo)
    # function to update winners, losses, ties columns in the database
    def updateUsersInfo(self, playersWL):
        with open("ConquianUsers.csv", mode='r') as usersFileR:
            usersFileReader = csv.DictReader(usersFileR, fieldnames= columnNames)
            updatedPlayerInfo = []

            for row in usersFileReader:
                for i in range(len(playersWL)):
                    if row["username"] == playersWL[i].get("username"):
                        row["wins"] = playersWL[i].get("wins")
                        row["losses"] = playersWL[i].get("losses")
                        row["ties"] = playersWL[i].get("ties")
                        updatedPlayerInfo.append(row)
        with open("ConquianUsers.csv", mode="w") as usersFileW:
            writer = csv.DictWriter(usersFileW, fieldnames=columnNames)
            for rows in updatedPlayerInfo:
                writer.writerow(rows)

    # function to allow players to switch cards
    def playersSwitchCards(self):
        self.playersSwitchCardsOut()
        self.playersSwitchCardsIn()
    def playersSwitchCardsOut(self):
        for i in range(self.numberOfPlayers):
            clear()
            print("{} Hand".format(self.playersInfo[i].get("username")))
            self.CardsSwitched.append(self.players[i].switchCardOut())
    def playersSwitchCardsIn(self):
        for i in range(self.numberOfPlayers):
            j = i + 1
            if(j == self.numberOfPlayers):
                j = 0
            self.players[j].switchCardIn(self.CardsSwitched[i])

# function to print the hands held by all the players, its debugging mechanism to help see where each card went
    def printHands(self):
        for i in range(self.numberOfPlayers):
            print(f"player {i} has")
            self.players[i].printHand()


# class for cards created via the deck Class
# current functions include creating new deck
# shuffle deck and print the deck
class Card(object):
    value = ""
    suit = ""
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def printCard(self):
        print("{} of {}".format(self.value, self.suit))
    def getCard(self):
        cardToPrint = "{} of {}".format(self.value, self.suit)
        return cardToPrint
# class for the deck to be created. it initiates the deck and then shuffles it.
# has a function to deal the top card of the deck to the next player and returns that card
# has function to deal cards to players
class Deck(object):
    def __init__(self):
        self.cards = []
        self.newDeck()
        self.shuffleDeck()
        self.LastCard = Card("empty", "empty")
    # create a new deck to play
    def newDeck(self):
        for suit in Suits:
            for val in Values:
                self.cards.append(Card(val, suit))
    # shuffle deck to get different variations of the deck everytime
    def shuffleDeck(self):
        numOfCards = 40
        for i in range(numOfCards):
            j = int(random() * i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
# function to deal the card on top of the deck
    def dealTopCard(self):
        cardsLeftCount = len(self.cards)
        if cardsLeftCount == 0:
            return False
        cardToreturn = self.cards[cardsLeftCount-1]
        self.cards.pop(cardsLeftCount-1)
        return cardToreturn
# function to deal all cards to initiate the game
    def dealCards(self, players, numberOfPlayers):
            for i in range(numberOfPlayers):
                players[i].getHand(self)
    # function to help end the game when running out of cards, and lead to a tie
    def getEmptyCard(self):
        return self.LastCard
# class for the player where it initiates the player already having his
# hand and the options the player has such as switching cards to start
# the game, draw card, playcard and discard card.
class Player(object):
    def __init__(self, cardCount):
        self.hand = []
        self.NumberCards = cardCount
        self.playedCards = []
        self.numberPlayedCards = 0
    # player has option to play card on the table or go a draw
    def pickUpCardOrNot(self, card):
        self.hand.append(card)
        self.printHand()
        validInput = False
        while not validInput:
            playOrDiscardOption = input("Do you want to play (1) or Discard this card(0) :")
            try:
                playOrDiscardOption = int(playOrDiscardOption)
                if playOrDiscardOption:
                    return True
                else:
                    self.discardCard()
                    return False
            except ValueError:
                validInput = False
    # function for each player to be dealt the cards.
    def getHand(self, deck):
        for i in range(self.NumberCards):
            self.hand.append(deck.dealTopCard())
    def returnCardAtPosition(self, position):
        return self.hand[position]
    def printPlayedCards(self):
        for card in self.playedCards:
            card.printCard()
    def returnPlayedCards(self):
        return self.playedCards
    def printHand(self):
        for card in self.hand:
            card.printCard()
    def switchCardOut(self):
        self.printHand()
        validposition = False
        while not validposition:
            positionToSwitch = input("enter position of card to Switch with Next Player:")
            try:
                positionToSwitch = int(positionToSwitch)
                if positionToSwitch < 9:
                    validposition = True
            except ValueError:
                validposition = False
        positionToSwitch = positionToSwitch -1
        switchCard = self.hand[positionToSwitch]

        self.hand.pop(positionToSwitch)
        return switchCard
    def switchCardIn(self, card):
        self.hand.append(card)
    def drawACard(self, deck):
        cardDrawn = deck.dealTopCard()
        if not cardDrawn:
            cardDrawn = deck.getEmptyCard()
            return cardDrawn
        self.hand.append(cardDrawn)
        self.printHand()
        validinput = False
        while not validinput:
            playerChoice = input("Do you wish to play card enter 1 or discard enter 0:")
            try:
                playerChoice = int(playerChoice)
                if playerChoice:
                    cardsToPlay = self.selectCardsToPlay()
                    if self.isPlayable(cardsToPlay):
                        self.playCards(cardsToPlay)
                        return self.discardCardAt()
                else:
                    return self.discardCard()
            except ValueError:
                validinput = False
    def discardCardAt(self):
        if len(self.hand) == 0:
            return False
        self.printHand()
        validPosition = False
        while not validPosition:
            positionOfCard2Discard = input("select position of Card to discard")
            try:
                positionOfCard2Discard = int(positionOfCard2Discard)
                if positionOfCard2Discard <= len(self.hand) and positionOfCard2Discard != 0:
                    validPosition = True
            except ValueError:
                validPosition = False
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
            self.numberPlayedCards = self.numberPlayedCards + 1
            if card in self.hand:
                self.hand.remove(card)
    def checkifWon(self):
        if len(self.hand) == 0:
            return True
        else:
            return False
    def selectCardsToPlay(self):
        finishSelecting = False
        cardsSelected = []
        while (finishSelecting == False):
            self.printHand()
            positionSelected = input("enter position of first two card to play and 9 to complete the set with the last card")
            try:
                positionSelected = int(positionSelected)
                if positionSelected == 9:
                    cardsSelected.append(self.returnCardAtPosition(len(self.hand) - 1))
                    finishSelecting = True
                    break
                if positionSelected <= len(self.hand):
                    cardsSelected.append(self.returnCardAtPosition(positionSelected - 1))
            except ValueError:
                finishSelecting = False
        return cardsSelected
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