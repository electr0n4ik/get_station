import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil.parser import parse

from base import Transaction, Station, Point


def get_token(url, login, password):
    # Версия установленного браузера должна совпадать с версией chromedriver
    # В этой проекте версия 126
    chrome_driver_path = '/snap/chromium/2897/usr/lib/chromium-browser/chromedriver'
    chrome_binary_path = '/usr/bin/google-chrome'
    token = None
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path
    chrome_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    try:
        driver.get(url=url)
        time.sleep(1)
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'userSigninLogin'))
        )
        password_field = driver.find_element(By.ID, 'userSigninPassword')
        username_field.send_keys('test')
        password_field.send_keys('v78ilRB63Y1b')
        password_field.send_keys(Keys.RETURN)
        time.sleep(1)
        account_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//title[text()='Аккаунт']"))
        )
        
        print(account_page.accessible_name)
        cookies = driver.get_cookies()

        for cookie in cookies:
            if cookie['name'] == 'testovaia_ploshhadaka_abakam_session':
                token = cookie['value']
                break
    
    except Exception as e:
        print(e)
    finally:
        driver.quit()

    return token

def extract_transactions(soup, credential, params_date):
    transactions = []
    from_date = params_date['from_date']
    to_date = params_date['to_date']
    table = soup.find_all("tr")

    for row in table:
        cols = row.find_all('td')
        transaction = Transaction()
        if len(cols) != 8:
            continue
        col_contract = cols[2].text.strip() if cols[2].text.strip() else None
        date_text = cols[1].text.strip()
        transaction_date = datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
        if not (from_date <= transaction_date <= to_date):
            continue
        if credential.contracts and col_contract not in credential.contracts:
            continue
        
        transaction = Transaction(credential = credential,
            station = Station(code = cols[4].text.strip() if cols[4].text.strip() else "",
                              point=Point(),),
            card = cols[3].text.strip() if cols[3].text.strip() else "",
            date = transaction_date,
            service = cols[5].text.strip() if cols[5].text.strip() else "",
            volume = int(cols[6].text.strip() if cols[6].text.strip() else 0),
            sum = int(cols[7].text.strip() if cols[7].text.strip() else 0))

        transactions.append(transaction)

    return transactions
