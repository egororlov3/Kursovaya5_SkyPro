from abc import ABC, abstractmethod
import requests


class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, query):
        pass


class HeadHunterAPI(JobAPI):
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query):
        print(f"Отправка запроса на получение вакансий для: {query}")
        response = requests.get(self.BASE_URL, params={"text": query})
        print("Запрос отправлен, ждем ответ...")
        response.raise_for_status()
        data = response.json()
        print("Ответ API:", data)  # Убедитесь, что ответ не слишком большой
        return data.get('items', [])

    def get_companies_and_vacancies(self, company_ids):
        vacancies = []
        for company_id in company_ids:
            response = requests.get(f"https://api.hh.ru/vacancies?employer_id={company_id}")
            response.raise_for_status()
            company_vacancies = response.json().get('items', [])
            vacancies.extend(company_vacancies)
        return vacancies
