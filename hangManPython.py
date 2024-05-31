import random
from enum import Enum
from pickle import FALSE
import array
from xml.etree.ElementTree import tostring

currentTarget = ""
userName = ""                                          

class gameState(Enum):  
    GUESSING = 1
    GAME_OVER = 2
    GAME_WON = 3
    QUIT = 4
 
targetBank = ["solvitur ambulando", 
              "all truly great thoughts are conceived by walking", 
              "the only emperor is the emperor of ice cream", 
              "dance first think later it is the natural order",
              "testing"]

lettersUsed = ['1'] 
gameWon = False
letterGuessed = 'a'
maxGuesses = 6 
remainingGuesses = 6 
hasQuit = False
currentState = gameState.GUESSING
puzzlePicker = random.randint(0, 4)

def drawGallows(state):
    print("-------+")
    if state == 0:
        print("|       ")
        print("|")
        print("|")
    elif state == 1:
        print("|      0")
        print("|")
        print("|")
    elif state == 2:
        print("|      0")
        print("|      |")
        print("|")
    elif state == 3:
        print("|      0")
        print("|      |")
        print("|       \\")
    elif state == 4:
        print("|      0")
        print("|      |")
        print("|     / \\")
    elif state == 5:
        print("|      0")
        print("|    --|")
        print("|     / \\")
    elif state == 6:
        print("|      0")
        print("|    --|--")
        print("|     / \\")
    pass
    print("|")
    print("+_______")
    print("+       +")

def welcomeMessage():
    print("Welcome to Hangman!")
    drawGallows(1)
    print("Please enter your name: ")
    userName = input()
    printedName = userName+"!"
    print("Welcome,",printedName)
    return userName
   
def displayCurrentGuessState():
    print (revealedAnswer)

def isGameOver(currentState, guessesLeft):
    if guessesLeft == 0:
        currentState = gameState.GAME_OVER
    return currentState

def isGameWon(revealedAnswer, target):
    result = False
    if revealedAnswer == target:
        result = True
    return result

def isLetterUsed(guessChar):
    result = False
    if lettersUsed.count(guessChar) > 0:
        result = True
    return result

def assessGuess(attempt):
    success = False
    if (currentTarget.count(attempt) > 0):
        success = True
        print("correct!!!")
    return success

def randomizeNewPuzzle():
    randomInt = random.randint(0,4)
    currentTarget = targetBank[randomInt]
    print("Here is your new puzzle:")
    return currentTarget

def generatePreReveal(target):
    puzzleIndex = 0
    while (puzzleIndex < len(target)):
        if target[puzzleIndex] != ' ':
            target[puzzleIndex] = '_'
        puzzleIndex = puzzleIndex + 1
    return target  

def guessing(revealed, target, guessesLeft, currentState):
    print("\nRemaining Guesses: ", remainingGuesses)
    print("\nGuess a letter: ");
    inputValue = input()
    letterGuessed = inputValue
    isUsed = isLetterUsed(letterGuessed)
    guessesDecrement = 0
    if isUsed == False:
        lettersUsed.append(letterGuessed)
        isCorrect = assessGuess(letterGuessed)
        if isCorrect:
            revealed = updateReveal(letterGuessed, revealed, target)
            revealed = "".join(revealed)
            if (isGameWon(revealed, target)): 
                currentState = gameState.GAME_WON
        else:
            guessesLeft = guessesLeft - 1
            currentState = isGameOver(currentState, guessesLeft)
    else:
            print("\n" + userName + ", you've used this letter already. \nPick another.");
    drawGallows(maxGuesses - guessesLeft)
    print(revealed)
    return guessesLeft, revealed, currentState
    
def resetGame():
    remainingGuesses = 6;
    currentTarget = targetBank[random.randint(0,4)]
    revealedAnswer = ""
    return remainingGuesses, currentTarget, revealedAnswer

def updateReveal(correctGuess, whatIsRevealed, target):
    index = 0
    whatIsRevealed = list(whatIsRevealed)
    target = list(target)
    while index < len(target):
        if (target[index] == correctGuess):
            whatIsRevealed[index] = correctGuess
        index = index + 1           
    return whatIsRevealed     

def gameOverRoutine():
    print("\nYou're dead!")

def gameWonRoutine():
    name = "\n"+userName;
    print(name,"won the round! Will", userName, "play again? Y/N")
    playAgain = input()
    if (playAgain == "Y"):
        currentState = gameState.GUESSING
    else:
        if (playAgain == "N"):
            currentState = gameState.QUIT
    return currentState        
            
userName = welcomeMessage()
currentTarget = randomizeNewPuzzle()
revealedAnswer = list(currentTarget)
drawGallows(maxGuesses - remainingGuesses);
revealedAnswer = generatePreReveal(revealedAnswer)
revealedAnswer = "".join(revealedAnswer)
print(revealedAnswer)

while (hasQuit == False):
    if (currentState == gameState.GUESSING):
        remainingGuesses, revealedAnswer, currentState = guessing(revealedAnswer, currentTarget, remainingGuesses, currentState)
    elif (currentState == gameState.GAME_OVER):
        gameOverRoutine()
        hasQuit = True
    elif (currentState == gameState.GAME_WON):
        currentState = gameWonRoutine()
        if (currentState == gameState.GUESSING):
            remainingGuesses, currentTarget, revealedAnswer = resetGame()
            lettersUsed.clear()
            revealedAnswer = list(currentTarget)
            revealedAnswer = generatePreReveal(revealedAnswer)
            revealedAnswer = "".join(revealedAnswer)            
    elif (currentState == gameState.QUIT):
        name = userName.upper() + "!"
        print("THANKS FOR PLAYING,",name,"GOOD BYE!")
        hasQuit = True
