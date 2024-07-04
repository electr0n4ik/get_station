import requests
from datetime import datetime
from bs4 import BeautifulSoup
from base import (BaseSystem,
                  Credential,
                  Transaction,
                  Station,
                  Point)
from service import *


class GasStationSystem(BaseSystem):
    base_url: str = 'https://test-app.avtoversant.ru'

    def auth(self, credential: Credential) -> None:
        url = credential.url if credential.url else self.base_url
        credential.token = get_token(url + "/account/login",
                                     credential.login,
                                     credential.password)
        print(f"Token: {credential.token}")
        self.credential = credential

    def get_transactions(self,
                         from_date: datetime,
                         to_date: datetime) -> list[Transaction]:
        credential = self.credential
        params = {
            'from_date': from_date.isoformat(),
            'to_date': to_date.isoformat()
        }
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en,ru;q=0.9,ru-RU;q=0.8,en-US;q=0.7",
            "Dnt": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "same-origin",
            "Sec-Fetch-Site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Cookie": f"testovaia_ploshhadaka_abakam_session={credential.token}"
        }
        # Если указаны номера контрактов, добавляем их в параметры запроса
        # if self.credential.contracts:
        #     params['contracts'] = self.credential.contracts
        
        # Отправка GET-запроса для получения транзакций
        response = self.connection.get(f'{credential.url}/account/transactions',
                                       headers=headers)  #,
                                    #    params=params)
        print("URL:", credential.url)
        print("Заголовки запроса:", headers)
        print("Статус код ответа:", response.status_code)
        print("Текст ответа:", response.text)
        # url = "https://test-app.avtoversant.ru/account/transactions?page_size=10&page=1"

        # Отправка запроса на сервер и получение HTML-кода страницы
        response = requests.get(f'{credential.url}/account/transactions')
        html = response.text

        # Парсинг HTML-кода с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        transactions_data = extract_transactions(soup)

        # for transaction in transactions_data:
        #     print(transaction)
        # Проверка успешности запроса
        # if response.status_code != 200:
        #     response.raise_for_status()
        # print("Test print", response.json())
        # transactions_data = response.json()
        # transactions = []
        
        # for data in transactions_data:
        #     if data['service'] == 'Пополнение баланса':
        #         continue
            
        #     transaction = Transaction(
        #         credential=self.credential,
        #         station=Station(
        #             code=data.get('station_code'),
        #             name=data.get('station_name'),
        #             brand=data.get('station_brand'),
        #             point=Point(
        #                 lat=data.get('station_lat', 0),
        #                 lng=data.get('station_lng', 0)
        #             ),
        #             address=data.get('station_address')
        #         ),
        #         card=data.get('card'),
        #         code=data.get('code'),
        #         date=datetime.fromisoformat(data.get('date')),
        #         service=data.get('service'),
        #         sum=float(data.get('sum', 0)),
        #         volume=float(data.get('volume', 0))
        #     )
        #     transactions.append(transaction)
        
        return 1  #transactions
