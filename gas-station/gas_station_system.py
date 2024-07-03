from datetime import datetime
from base import BaseSystem, Credential, Transaction


class GasStationSystem(BaseSystem):
    base_url: str = 'https://test-app.avtoversant.ru'

    # нужно реализовать этот класс
    
    def auth(self, credential: Credential) -> None:
        raise NotImplementedError()
    
    def get_transactions(self, from_date: datetime, to_date: datetime) -> list[Transaction]:
        raise NotImplementedError()

