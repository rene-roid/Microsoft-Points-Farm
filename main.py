import json
import random
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
from dotenv import load_dotenv


def wait_for(sec=2):
    time.sleep(sec)


def Search_random_words(driver):
    randomlists_url = "https://www.randomlists.com/data/words.json"
    response = requests.get(randomlists_url)
    words_list = random.sample(json.loads(response.text)['data'], 60)
    print('{0} words selected from {1}'.format(len(words_list), randomlists_url))

    url_base = 'http://www.bing.com/search?q='
    wait_for(5)
    for num, word in enumerate(words_list):
        print('{0}. URL : {1}'.format(str(num + 1), url_base + word))
        try:
            driver.get(url_base + word)
            # Print 'h2' tag text
            print('\t' + driver.find_element('css selector', 'h2').text)
        except Exception as e1:
            print(e1)
        wait_for()


# Load environment variables from .env file
load_dotenv()

def LoginPC(driver):
    wait_for(1)
    driver.get("https://login.live.com")
    wait_for(1)

    try:
        elem = driver.find_element('css selector', '[name="loginfmt"]')
        elem.clear()
        elem.send_keys(os.getenv("USERNAME"))  # Retrieve username from .env file
        elem.send_keys(Keys.RETURN)
        wait_for(5)
        elem1 = driver.find_element('css selector', '[name="passwd"]')
        elem1.clear()
        elem1.send_keys(os.getenv("PASSWORD"))  # Retrieve password from .env file
        elem1.send_keys(Keys.ENTER)
        wait_for(3)
    except Exception as e:
        print(e)
        wait_for(4)

    StaySignedIn(driver)


def StaySignedIn(driver):
    try:
        elem = driver.find_element('xpath',
                                   '/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[1]')
        elem.click()
        wait_for(3)
    except Exception as e:
        print(e)
        wait_for(4)


def GetPcRewards():
    # Driver path C:\C Folders\Drivers\sedgedriver.exe
    service = Service('./msedgedriver.exe')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(service=service)

    # LoginPC(driver)
    Search_random_words(driver)

    driver.close()


def GetDailyRewards():
    # Driver path C:\C Folders\Drivers\edgedriver_win64\MicrosoftWebDriver.exe
    service = Service('./msedgedriver.exe')
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Edge(service=service)

    # LoginPC(driver)
    MicrosoftDaily(driver)
    DoExtras(driver)

    driver.close()


def MicrosoftDaily(driver):
    wait_for(1)
    driver.get("https://rewards.bing.com")
    wait_for(1)

    for num in range(1, 4):
        try:
            xpath_element = "//*[@id=\"daily-sets\"]/mee-card-group[1]/div/mee-card[" + str(
                num) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a'
            print("Clicking on " + xpath_element)
            elem = driver.find_element('xpath', xpath_element)
            elem.click()

            wait_for(2)

            # switch to new tab
            driver.switch_to.window(driver.window_handles[1])
            CheckCookies(driver)

            if IsSuperSonicTest(driver):
                DoSuperSonicTest(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            elif IsDailyTest(driver):
                DoDailyTest(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                wait_for(2)
                # Close the new tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            wait_for(1)

        except Exception as e:
            print(e)
            wait_for(4)


def CheckCookies(driver):
    try:
        elem = driver.find_element('xpath', '//*[@id="bnp_btn_accept"]')
        elem.click()
        wait_for(1)
        print("Found cookies")
    except Exception as e:
        print("Not found cookies")
        return False


def IsSuperSonicTest(driver):
    try:
        elem = driver.find_element('xpath', '//*[@id="rqStartQuiz"]')
        print("Found super sonic test")
        return True
    except Exception as e:
        print("Not found super sonic test")
        return False


def DoSuperSonicTest(driver):
    try:
        DoLogin(driver)
        wait_for(1)
        start = driver.find_element('xpath', '//*[@id="rqStartQuiz"]')
        start.click()
        wait_for(2)

        num = 0
        breakCount: int = 0
        resetCount: int = 0
        while num < 9:
            try:
                elem = FindCorrectXpath(driver, num)
                if elem is False:
                    num = 0
                    resetCount += 1
                    if resetCount > 4:
                        break
                    pass
                else:
                    ClickButton(elem)
                num += 1
                wait_for(2)
            except Exception as e:
                print(e)
                wait_for(4)
                # reset for loop
                num = 0
                breakCount += 1

                if breakCount > 4:
                    break

    except Exception as e:
        print(e)
        wait_for(4)


def ClickButton(element):
    try:
        element.click()
        wait_for(4)
    except Exception as e:
        print(e)
        wait_for(4)


def FindCorrectXpath(driver, num):
    xpath1 = '//*[@id="rqAnswerOption' + str(num) + '"]'

    try:
        elem = driver.find_element('xpath', xpath1)
        return elem
    except Exception as e:
        print(e)
        return False


def IsDailyTest(driver):
    try:
        elem = driver.find_element('xpath', '//*[@id="btoption0"]')
        print("Found daily test")
        return True
    except Exception as e:
        print("Not found test")
        return False


def DoDailyTest(driver):
    try:
        DoLogin(driver)
        wait_for(1)
        start = driver.find_element('xpath', '//*[@id="btoption0"]')
        start.click()
        wait_for(2)

    except Exception as e:
        print(e)
        wait_for(4)


def DoLogin(driver):
    try:
        wait_for(1)
        btn_path = "/html/body/div[2]/div[2]/span/a"
        elem = driver.find_element('xpath', btn_path)
        elem.click()
        wait_for(1)
        print("Found login button")
        CheckCookies(driver)
    except Exception as e:
        print("Not found login button")
        return False


def DoExtras(driver):
    wait_for(1)
    driver.get("https://rewards.bing.com")
    wait_for(1)

    try:
        parent_xpath = '//*[@id="more-activities"]'
        child_xpath = parent_xpath + '/div/mee-card'

        # Get all child elements, click on each element, and close the tab
        child_elements = driver.find_elements('xpath', child_xpath)
        for index, element in enumerate(child_elements, start=1):
            element_xpath = child_xpath + f'[{index}]'
            element.click()
            driver.switch_to.window(driver.window_handles[1])
            if IsSuperSonicTest(driver):
                DoSuperSonicTest(driver)
            wait_for(1)
            driver.close()  # Close the tab
            driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window
            wait_for(1)

    except Exception as e:
        print(e)
        wait_for(4)


def MobileRewards():
    options = Options()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    # driver = webdriver.Firefox(options=options, executable_path=r'C:\C Folders\Drivers\geckodriver.exe')
    driver = webdriver.Firefox(options=options)

    LoginPC(driver)
    wait_for(1)

    try:
        # //*[@id="id_a"]
        driver.get("http://www.bing.com/search?q=bing+rewards")
        wait_for(3)
        cookies = driver.find_element('xpath', '//*[@id="bnp_btn_accept"]')
        cookies.click()
        wait_for(1)
        elem = driver.find_element('xpath', '//*[@id="id_a"]')
        elem.click()
        wait_for(3)
    except Exception as e:
        print(e)
        wait_for(4)

    Search_random_words(driver)

# GetDailyRewards()
GetPcRewards()
# MobileRewards()
