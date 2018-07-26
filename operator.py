from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import time
import re
import numpy as np

#username and password used to sign in
username = "esslushy"
password = "l1o2l3o4"
#signing in
driver = webdriver.Chrome()
driver.get("https://www.wajas.com/home_landing.php")
usernameInput = driver.find_element_by_id("username")
passwordInput = driver.find_element_by_id("password")
usernameInput.send_keys(username)
passwordInput.send_keys(password)
submitButton = driver.find_element_by_class_name("login-button")
submitButton.click()
gameButton = driver.find_element_by_id("td-games")
gameButton.click()
mastermindButton = driver.find_element_by_xpath('//a[@href="/world_game_mastermind_intro.php"]')
mastermindButton.click()
try:
    startGameButton = driver.find_element_by_xpath('//a[@href="world_game_mastermind.php"]')
    startGameButton.click()
except NoSuchElementException:
    print("already on page")
#colors to numbers
red = 0
orange = 1
yellow = 2
green = 3
blue = 4
purple = 5
def getResult():
    try:
        result = driver.find_element_by_class_name("game-waw-result")
        return re.sub(r'\([^)]*\)', "", result.text)
    except NoSuchElementException:
        return None
    except ElementNotVisibleException:
        return None
def parseResult(result):
    parsedResult = re.sub(r'[a-zA-Z+.]', "", result)
    parsedResult = parsedResult.split()
    if len(parsedResult) is 2:
        return (int(parsedResult[0]), int(parsedResult[1]))
    elif len(parsedResult) is 1:
        if "found" in result:
            return (int(parsedResult[0]), 0)
        else:
            return (0, int(parsedResult[0]))
    else:
        return (0, 0)
def inputSelectionOfCode(choice):
    #getting and using game waw pickers
    allGameWawPickers = driver.find_elements_by_class_name("game-waw-picker")
    firstWaw = allGameWawPickers[0:6]
    secondWaw = allGameWawPickers[6:12]
    thirdWaw = allGameWawPickers[12:18]
    fourthWaw = allGameWawPickers[18:]

    firstWaw[choice[0]].click()
    time.sleep(.1)
    secondWaw[choice[1]].click()
    time.sleep(.1)
    thirdWaw[choice[2]].click()
    time.sleep(.1)
    fourthWaw[choice[3]].click()
    time.sleep(.1)
    submitColorWawButton = driver.find_element_by_class_name("game-waw-button")
    submitColorWawButton.click()
    time.sleep(1.2)
def checkIfWon():
    #try to restart game if able/ if won
    try:
        playAgainButton = driver.find_element_by_xpath("//div[text()='Start a new game']")
        playAgainButton.click()
        print("game ended")
        return True
    except NoSuchElementException:
        print("Still in game")
        return False
def figureOutNextGuess():
    

#code
results = {}
i=1
while(True):
    guess = []
    if i is 1:
        guess = figureOutNextGuess()
    else:
        guess = figureOutNextGuess()#array of 4 "colors" but are actually numbers
    inputSelectionOfCode(guess)
    if(checkIfWon()):
        results = {}
        i=0
        time.sleep(1)
    else:
        result = parseResult(getResult())#tuple of Black, white or correct place and color and just correct place
        results[i]={"guess": guess, "result": result}
        i+=1
    