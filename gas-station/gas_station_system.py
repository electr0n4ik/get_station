import requests
from datetime import datetime
from bs4 import BeautifulSoup
from base import BaseSystem, Credential, Transaction
from service import get_token, extract_transactions


class GasStationSystem(BaseSystem):
    base_url: str = "https://test-app.avtoversant.ru"

    def auth(self, credential: Credential) -> None:
        url = credential.url if credential.url else self.base_url
        credential.token = get_token(
            url + "/account/login", credential.login, credential.password
        )
        self.credential = credential

    def get_transactions(
        self, from_date: datetime, to_date: datetime
    ) -> list[Transaction]:
        credential = self.credential
        params_date = {"from_date": from_date, "to_date": to_date}
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
            "Cookie": f"testovaia_ploshhadaka_abakam_session={credential.token}",
        }

        response = self.connection.get(
            f"{credential.url}/account/transactions?page_size=100&page=1",
            headers=headers,
        )
        transactions = []
        page = 1
        while True:
            response = requests.get(
                f"{credential.url}/account/transactions?page_size=100&page={page}",
                headers=headers,
            )
            if response.status_code != 200:
                break
            soup = BeautifulSoup(response.text, "lxml")
            page_transactions = extract_transactions(soup, credential, params_date)
            if not page_transactions:
                break
            transactions.extend(page_transactions)
            page += 1

        return transactions
