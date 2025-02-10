import os
import time
import re
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')


def sleep(milliseconds):
    time.sleep(milliseconds / 1000)

def click(driver, text):
    element = driver.find_element(By.XPATH, f"//*[text()='{text}']")
    element.click()

def click_by_xpath(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()

def compare_occurrences_and_rename():
    current_file = 'current_table.html'
    previous_file = 'previous_table.html'

    try:
        if not os.path.exists(previous_file):
            shutil.move(current_file, previous_file)
            print('First run of the script, renamed current_table.html to previous_file.html')
            return

        with open(current_file, 'r', encoding='utf-8') as file:
            current_data = file.read()
        with open(previous_file, 'r', encoding='utf-8') as file:
            previous_data = file.read()

        occurrences_current_bestanden = len(re.findall('bestanden', current_data))
        occurrences_current_nicht_bestanden = len(re.findall('nicht bestanden', current_data))
        occurrences_previous_bestanden = len(re.findall('bestanden', previous_data))
        occurrences_previous_nicht_bestanden = len(re.findall('nicht bestanden', previous_data))

        if (occurrences_current_bestanden != occurrences_previous_bestanden or
                occurrences_current_nicht_bestanden != occurrences_previous_nicht_bestanden):
            shutil.move(current_file, previous_file)
            print('New grades added')
            requests.get(f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=New%20grades%20have%20been%20added')
        else:
            print("nothing happened")
    except Exception as e:
        print('Error occurred:', e)

def open_google():
    options = Options()
    options.headless = True
    # Uncomment the following line if you want to run headless in linux server and comment the second driver line

    #service = Service("/usr/bin/chromedriver")  # Specify the path to the ChromeDriver binary
    #driver = webdriver.Chrome(service=service, options=options)

    driver = webdriver.Chrome(options=options)
    try:
        driver.get('https://qis.hs-albsig.de/')
        sleep(1000)
        driver.find_element(By.NAME, 'asdf').send_keys(username)
        sleep(1000)
        driver.find_element(By.NAME, 'fdsa').send_keys(password, Keys.RETURN)
        sleep(2000)
        click(driver, 'Prüfungsverwaltung')
        sleep(1000)
        click(driver, 'Notenspiegel')
        sleep(1000)
        click_by_xpath(driver, "//img[@alt='Leistungen für Abschluss 84 Bachelor anzeigen']")

        sleep(2000)

        table_element = driver.find_element(By.XPATH, "//th[contains(., 'Bachelor')]/ancestor::table[1]")
        table_html = table_element.get_attribute('innerHTML')

        with open('current_table.html', 'w', encoding='utf-8') as file:
            file.write(table_html)

        compare_occurrences_and_rename()

        click_by_xpath(driver, "//a[contains(@href, 'auth.logout')]")
    finally:
        driver.quit()

def run_code():
    try:
        now = time.localtime()
        hours = now.tm_hour

        if 7 <= hours <= 23:
            open_google()
    except Exception as e:
        print('error', e)

def schedule_run_code():
    while True:
        interval_minutes = get_random_interval()
        delay_seconds = interval_minutes * 60
        sleep(delay_seconds * 1000)
        run_code()

def get_random_interval():
    min_minutes = 15
    max_minutes = 30
    return random.randint(min_minutes, max_minutes)

if __name__ == "__main__":
    run_code()
    schedule_run_code()