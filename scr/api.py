from abc import ABC, abstractmethod
import requests


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query):
        pass


class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query):
        response = requests.get(self.BASE_URL, params={"text": query})
        response.raise_for_status()
        data = response.json()
        print("Ответ API:", data)
        return data.get('items', [])


