import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil.parser import parse
from base import InvalidCredentialsError


def get_token(url, login, password):
    #TODO: add env
    chrome_driver_path = '/snap/chromium/2897/usr/lib/chromium-browser/chromedriver'
    #TODO: add env
    chrome_binary_path = '/usr/bin/google-chrome'
    token = None
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path
    chrome_service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    try:
        driver.get(url=url)

        # if response.status_code != 200:  # or 'token' not in response.json():
        #     print("Test print", response.json())
        #     raise InvalidCredentialsError("Invalid login or password")
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
        
        #     # Пример: Извлекаем имя пользователя из меню
        #     user_menu = driver.find_element(By.ID, 'dropdown01')
        #     username = user_menu.text
        #     print('Имя пользователя:', username)

        #     menu_links = driver.find_elements(By.CSS_SELECTOR, '.nav-link')
        #     for link in menu_links:
        #         print('Ссылка:', link.get_attribute('href'), '| Текст:', link.text)
            
        # else:
        #     raise InvalidCredentialsError("Invalid login or password")
    
    except Exception as e:
        print(e)
    finally:
        driver.quit()

    return token

def extract_transactions(soup):
    transactions = []
    table = soup.find_all('div')
    # table = soup.find(name='table', attrs={'table': 'table'})
    print(table)
    # rows = table.find_all('tr')[1:]  # Пропустить заголовок таблицы

    # for row in rows:
    #     cols = row.find_all('td')
    #     transaction = {
    #         'Номер': cols[0].text.strip(),
    #         'Дата': parse(cols[1].text.strip()),
    #         'Контракт': cols[2].text.strip(),
    #         'Карта': cols[3].text.strip(),
    #         'АЗС': cols[4].text.strip(),
    #         'Товар': cols[5].text.strip(),
    #         'Объем': int(cols[6].text.strip()),
    #         'Сумма': int(cols[7].text.strip())
    #     }
    #     transactions.append(transaction)

    return "transactions"