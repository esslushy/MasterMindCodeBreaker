from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
import time, re, collections, itertools, math, random
import numpy as np
import pandas as pd

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

def getResult():
    try:
        result = driver.find_element_by_class_name("game-waw-result")
        return re.sub(r'\([^)]*\)', "", result.text)
    except NoSuchElementException as err:
        print(err)
        return None
    except ElementNotVisibleException as err:
        print(err)
        return None
    except AttributeError as err:
        print(err)
        return None
def scoringResult():
    result = getResult()
    try:
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
    except TypeError:
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
#code for building game
def givenum():#return random 4 digit number with duplicate
    num = []
    for i in range(4):
        num.append(random.randrange(0,6))
    return tuple(num)
def playresult(notknow, guess):
    A = 0
    B = 0
    for idx, val in enumerate(notknow):
        for idx2, val2 in enumerate(guess):
            if guess[idx] == val:
                A+=1
                break
            elif(val == val2):
                B+=1
                break
    return A, B
def ini_population():#make all possible guesses
    return list([p for p in itertools.product(range(0,6), repeat=4)])
def chooseOne(code_set):
    remain_table = np.zeros(len(code_set))
    for idx, val in enumerate(code_set):
        code_idx = [j for j in range(len(code_set))]
        code_idx.remove(idx)
        if(len(code_idx) > 100):
            S = random.sample(code_idx, 100)
        else:
            S = random.sample(code_idx, len(code_idx))
        remain = 0
        for idxx in S:
            A, B = playresult(code_set[idxx], code_set[idx])
            for k in S:
                a, b = playresult(code_set[k], code_set[idx])
                if (a==A and b==B):
                    remain+=1
        remain_table[idx]=remain
    mindex = np.argmin(remain_table)
    return code_set[mindex]
#code for building game
#code 
masterCodeSet = ini_population()
while(True):#fresh start
    continuePlaying = True
    results = {}
    i=1
    guess = []
    code_set = masterCodeSet#the population basically all the guesses from red red red red to purple purple purple purple
    while(continuePlaying):#once won everything resets
        if i == 1:#first guess
            guess = (0, 0, 1, 1)#best guess according to knuth
            print(guess)
            inputSelectionOfCode(guess)
        else:#all the rest
            tempCodeSet =[]
            for t in code_set:
                tempResult = playresult(t, results[i-1]["guess"])
                if  tempResult[0] == results[i-1]["result"][0]:
                    tempCodeSet.append(t)
                    #sort them all out according to previous results
            code_set = tempCodeSet
            guess = chooseOne(code_set)
            print(guess)
            inputSelectionOfCode(guess)
        if(checkIfWon()):
            continuePlaying = False
        else:
            result = scoringResult()#tuple of Black, white or correct place and color and just correct place
            print(result)
            results[i]={"guess": guess, "result": result}
            i+=1
    time.sleep(1)#just in case
    