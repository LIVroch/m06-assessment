from config import dictionaryLoc
from config import turnTextLoc
from config import wheelTextLoc
from config import maxRounds
from config import vowelCost
from config import roundStatusLoc
from config import finalPrize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""}}

roundNum = 0
dictionary = []
wheelList = []
hintPhrase = []
vowels = {"A", "E", "I", "O", "U"}

def readFileIntoList(txt, list):
    # read file in from file location
    file = open(txt)
    value = file.readlines()
    file.close()
    # store each phrase in a list
    for i in range(len(value)):
        list.append(str(value[i]).upper().strip().replace(r"\\n",""))
    return list
   
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    playerOne = input("Enter Player 1's name: ").strip().capitalize()
    players[0]["name"] = playerOne
    playerTwo = input("Enter Player 2's name: ").strip().capitalize()
    players[1]["name"] = playerTwo
    playerThree = input("Enter Player 3's name: ").strip().capitalize()
    players[2]["name"] = playerThree
    return players
     
def gameSetup():  
    # read dictionary and wheeldata files into lists
    # read status messages files into variables
    readFileIntoList(dictionaryLoc, dictionary)
    readFileIntoList(wheelTextLoc, wheelList)
    getPlayerInfo()
# gameSetup()
    
def getPhrase():
    global roundPhrase
    global phraseList
    global hintPhrase
    # choose random phrase from dictionary
    fate = int((random.random()) * (len(dictionary)))
    roundPhrase = dictionary[fate]
    # make a list of the phrase with underscores instead of letters
    phraseList = list(roundPhrase)
    listCopy = phraseList.copy()
    for i in range(len(listCopy)):
        if str(listCopy[i-1]).isalpha() == True:
            listCopy[i-1] = "_"
            hintPhrase = listCopy
    return roundPhrase, hintPhrase

def wofRoundSetup():
    global players
    global roundPhrase
    global hintPhrase
    global initPlayer
    global vowels
    vowels = {"A", "E", "I", "O", "U"}
    # set round total for each player = 0
    players[0]["roundtotal"] = 0
    players[1]["roundtotal"] = 0
    players[2]["roundtotal"] = 0
    # return the starting player number (random)
    fate = int((random.random()) * 3)
    initPlayer = fate
    # use getPhrase function to retrieve the roundPhrase and hintPhrase
    getPhrase()
    return initPlayer
# wofRoundSetup()
# print(initPlayer)
# print(roundPhrase)

def guessConsonant():
    # take in a player number 
    global players
    global hintPhrase
    global goodGuess
    global count
    # ensure letter is a consonant
    goodGuess = False
    count = 0
    consonant = "n"
    while consonant == "n":
        conGuess = input("Guess a consonant: ").upper().strip()
        if conGuess not in vowels:
            consonant = "y" 
            # return goodGuess= true if it was a correct guess
            for i in range(len(phraseList)):
                if phraseList[i] == conGuess:
                    goodGuess = True
                    # return count of letters in phrase
                    count = roundPhrase.count(conGuess) 
                    # change position of found letter in hintPhrase to the letter instead of underscore
                    hintPhrase[i] = conGuess
        else:
            print("Invalid input, expecting a consonant.") 
    return goodGuess, count

def spinWheel(playerNum):
    # take in a player number
    global wheelList
    global players
    global vowels
    # get random value for wheelList
    fate = int(random.random() * len(wheelList))
    wheelSpin = wheelList[fate]
    print("The wheel spins...")
    print(f"{wheelSpin}!")
    # check for BANKRUPT, and take action
    if wheelSpin == "BANKRUPT":
        players[playerNum]["roundtotal"] = 0
        print("Your round total has been reset, and your turn is over.")
        stillInTurn = False
    # check for LOSE A TURN
    elif wheelSpin == "LOSE A TURN":
        print("Your turn is over.")
        stillInTurn = False
    # get amount from wheel if not LOSE A TURN or BANKRUPT
    else:
        wheelAmount = int(wheelSpin)
        print(f"Guess a letter correctly and add ${wheelAmount} to your round total.")
    # use guessLetter function to see if guess is in phrase and return count
        guessConsonant()
    # change player round total if they guess right
        if goodGuess == True:
            players[playerNum]["roundtotal"] = players[playerNum]["roundtotal"] + wheelAmount
            roundTotal = players[playerNum]["roundtotal"]
            stillInTurn = True
            print("Correct!")
            print(f"There are {count} instances of that letter in the phrase.")
            print(hintPhrase)
            print(f"Nice guess! Your round total is now ${roundTotal}.")
        else:
            stillInTurn = False
            print("Better luck next time! Your turn is over.")
    return stillInTurn
# spinWheel(1)

def guessVowel():
    # take in a player number 
    global players
    global hintPhrase
    global goodGuess
    global count
    # ensure letter is a vowel
    goodGuess = False
    vowel = "n"
    while vowel == "n":
        vowGuess = input("Guess a vowel: ").strip().upper()
        if vowGuess in vowels:
            vowel = "y" 
            # return goodGuess= true if it was a correct guess
            for i in range(len(phraseList)):
                if phraseList[i] == vowGuess:
                    goodGuess = True
                    # return count of letters in phrase.
                    count = roundPhrase.count(vowGuess) 
                    # change position of found letter in hintPhrase to the letter instead of underscore
                    hintPhrase[i] = vowGuess
            vowels.discard(vowGuess)
        else:
            print("Invalid input, expecting a vowel that hasn't been guessed yet.") 
    return goodGuess, count

def buyVowel(playerNum):
    # take in a player number
    global players
    global vowels
    # ensure player has 250 required for buying a vowel
    roundTotal = players[playerNum]["roundtotal"]
    if vowels != set():
        if roundTotal >= 250:
            roundTotal = roundTotal - 250
            print(f"Transaction accepted, your total is now ${roundTotal}.")
        # use guessVowel function to see if the letter is in the file
            guessVowel()
            if goodGuess == True:
                print("Correct!")
                print(f"There are {count} instances of that letter in the phrase.")
                print(hintPhrase) 
                print("Nice Guess!")
                stillInTurn = True
            else:
                print("Better luck next time!")
                stillInTurn = True
        else:
            print(f"Your total of ${roundTotal} is not enough to afford a vowel.")
            stillInTurn = True
    else:
        print("There are no more vowels to guess.")
        stillInTurn = True
    return stillInTurn
# buyVowel(1)
# print(vowels)
        
def guessPhrase(playerNum):
    # take in player number
    global players
    global hintPhrase
    global roundPhrase
    # ask for input of the phrase
    print(hintPhrase)
    phraseGuess = list(input("Guess the full phrase: ").strip().upper())
    # check if it is the same as roundPhrase
    if phraseGuess == phraseList:
        print("Correct!\nThe guessed phrase matches the round phrase.")
        # fill in hintPhrase with letters instead of underscores if correct
        for i in range(len(phraseList)):
            hintPhrase[i] = phraseGuess[i]
        print(hintPhrase)
        stillInRound = False
    else:
        stillInRound = True
    return stillInRound
# guessPhrase()
    
def wofTurn(playerNum):  
    # take in a player number
    global roundPhrase
    global hintPhrase
    global players
    # do all turn related activity including update roundtotal     
    stillInTurn = True
    stillInRound = True
    while stillInTurn == True:
        # use the string.format method to output your status for the round
        currentPlayer = players[playerNum]["name"]
        roundTotal = players[playerNum]["roundtotal"]
        print(f"It is currently {currentPlayer}'s turn, they have ${roundTotal} in their round bank.")
        # get user input S for spin, B for buy a vowel, G for guess the phrase
        print(hintPhrase)
        choice = input("Enter a letter to (s)pin the wheel, (b)uy a vowel, or (g)uess the phrase: ")
        if(choice.strip().upper() == "S"):
            stillInTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillInTurn = buyVowel(playerNum)
        elif(choice.upper() == "G"):
            stillInRound = guessPhrase(playerNum)
            stillInTurn = False
        else:
            print("Not a correct option")
    print(f"End of turn. {currentPlayer} ends this turn with ${roundTotal} in their round bank.")
    return stillInRound
# wofTurn(1)

def wofRound():
    global players
    global roundPhrase
    global hintPhrase
    global totalBanked
    initPlayer = wofRoundSetup()
    # keep doing things in a round until the phrase is solved
    currPlayer = initPlayer
    print("New Round!")
    print("New phrase:")
    print(f"Hint: **{roundPhrase}**")
    print(hintPhrase)
    stillInRound = True
    while stillInRound == True:
        # while still in the round keep rotating through players
        while currPlayer < 3:
            stillInRound = wofTurn(currPlayer)
            win = currPlayer
            currPlayer = currPlayer + 1
            if stillInRound == False:
                break
        currPlayer = 0
    # tell people the state of the round as you are leaving a round
    print("End of round!")
    roundWinnings = players[win]["roundtotal"]
    totalBanked = players[win]["gametotal"] + roundWinnings
    players[win]["gametotal"] = totalBanked
    winner = players[win]["name"]
    print(f"{winner} has guessed the word correctly and banked ${totalBanked} overall.")
    return totalBanked
# wofRound()

def guessAftermath():
    if goodGuess == True:
        print("Correct!")
        print(f"There are {count} instances of that letter in the phrase.")
        print(hintPhrase)
    else:
        print("Incorrect.")
        print(hintPhrase)

def wofFinalRound():
    global roundPhrase
    global hintPhrase
    winplayer = 0
    amount = 0
    playerTotals = {}
    # find highest gametotal player
    for i in players.keys():
        playerTotals[i] = players[i]["gametotal"]
    print(playerTotals)
    mostBankList = [key for key in playerTotals if (playerTotals[key] == max(playerTotals.values()))]
    mostBankIndex = mostBankList[0]
    print(mostBankIndex)
    # print out instructions for that player and who the player is
    finalPlayer = players[mostBankIndex]["name"]
    playerBank = players[mostBankIndex]["gametotal"]
    print(f"Final Round!\nOur final contestant is {finalPlayer} with a total of ${playerBank} banked.")
    # Use the getPhrase function to reset the roundPhrase and the hintPhrase
    getPhrase()
    print("New phrase:")
    print(f"Hint: **{roundPhrase}**")
    print(hintPhrase)
    # check for ['R','S','T','L','N','E']
    freeHint = ['R','S','T','L','N','E']
    while freeHint != []:
        for i in range(len(phraseList)):
            if freeHint[0] == phraseList[i]:
                hintPhrase[i] = freeHint[0]
        freeHint.remove(freeHint[0])
    print(hintPhrase)
    # gather 3 consonants and 1 vowel and use the guessletter function to see if they are in the phrase
    guessConsonant()
    guessAftermath()

    guessConsonant()
    guessAftermath()

    guessConsonant()
    guessAftermath()

    guessVowel()
    guessAftermath()
    # get user to guess phrase
    phraseGuess = list(input("Guess the full phrase: ").strip().upper())
    # check if it is the same as roundPhrase
    if phraseGuess == phraseList:
        print("Correct!\nThe guessed phrase matches the round phrase.")
        # fill in hintPhrase with letters instead of underscores if correct
        for i in range(len(phraseList)):
            hintPhrase[i] = phraseGuess[i]
        print(hintPhrase)
        # if they do, add finalprize and gametotal and print out that the player won
        playerBank = playerBank + finalPrize
        print(f"Congratulations!\n{finalPlayer} won the grand prize of ${finalPrize}!")
        print(f"Their final total is ${playerBank}.")
    else:
        print(f"Aww... {finalPlayer} failed miserably.\nThere is no consolation prize :)")
        print(f"Their final total is ${playerBank}.")
# wofFinalRound()

def main():
    gameSetup()    

    for i in range(0,maxRounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()