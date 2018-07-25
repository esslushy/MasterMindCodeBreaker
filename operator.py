from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
except selenium.common.exceptions.ElementNotVisibleException:
    print("already on page")
#getting and using game waw pickers
allGameWawPickers = driver.find_elements_by_class_name("game-waw-picker")
#colors to numbers
red = 0
orange = 1
yellow = 2
green = 3
blue = 4
purple = 5
firstWaw = allGameWawPickers[0:6]
secondWaw = allGameWawPickers[6:12]
thirdWaw = allGameWawPickers[12:18]
fourthWaw = allGameWawPickers[18:]

firstWaw[yellow].click()
secondWaw[red].click()
thirdWaw[purple].click()
fourthWaw[green].click()

