from databases_src.db_manager import DBManager
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver


class DataFetcher:
    def __init__(self):
        self.hh_api = HeadHunterAPI()
        self.json_saver = JSONSaver()
        self.db_manager = DBManager()

    def fetch_vacancies_for_companies(self, companies):
        all_vacancies = []  # Список для хранения всех вакансий
        for company in companies:
            print(f"Получение вакансий для компании: {company}")
            vacancies = self.hh_api.get_vacancies(company)
            vacancies_list = Vacancy.cast_to_object_list(vacancies)

            # Сохраняем компанию в базу данных
            self.db_manager.save_company(company)

            for vacancy in vacancies_list:
                print(f"Создаем вакансию: {vacancy.title}")
                self.json_saver.add_vacancy(vacancy)
                self.db_manager.save_vacancy(vacancy)  # Теперь сохраняем вакансию в БД
                all_vacancies.append(vacancy)

        print("Вакансии сохранены!")
        return all_vacancies

    def filter_vacancies_by_salary(self, vacancies, min_salary=None, max_salary=None):
        salary_filtered_vacancies = []
        for vacancy in vacancies:
            salary = vacancy.get_salary()
            if (min_salary is None or (salary is not None and salary >= min_salary)) and \
                    (max_salary is None or (salary is not None and salary <= max_salary)):
                salary_filtered_vacancies.append(vacancy)
        return salary_filtered_vacancies

    def filter_vacancies_by_keyword(self, vacancies, keyword):
        unique_vacancies = set()
        filtered_vacancies = []

        for vacancy in vacancies:
            # Проверка названия и описания вакансии
            if (vacancy.title and keyword.lower() in vacancy.title.lower()) or \
                    (vacancy.description and keyword.lower() in vacancy.description.lower()):
                unique_vacancies.add(vacancy)
                filtered_vacancies.append(vacancy)

        return filtered_vacancies


def print_vacancies(vacancies):
    if not vacancies:
        print("Нет доступных вакансий")
        return

    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}\n")


def main():
    data_fetcher = DataFetcher()

    companies = [
        'Яндекс', 'Сбер', 'Тинькофф', 'Газпром', 'Авито',
        'SkyEng', 'МТС', 'Альфа-Групп', 'ВТБ', 'Ростелеком'
    ]

    all_vacancies = data_fetcher.fetch_vacancies_for_companies(companies)

    # Ввод минимальной зарплаты
    min_salary_input = input("Введите минимальную зарплату (или оставьте пустым для пропуска): ")
    min_salary = int(min_salary_input) if min_salary_input else None

    # Ввод максимальной зарплаты
    max_salary_input = input("Введите максимальную зарплату (или оставьте пустым для пропуска): ")
    max_salary = int(max_salary_input) if max_salary_input else None

    keyword = input("Введите ключевое слово для фильтрации вакансий: ").lower()

    salary_filtered_vacancies = data_fetcher.filter_vacancies_by_salary(all_vacancies, min_salary, max_salary)

    # Фильтрация по ключевому слову
    filtered_vacancies = data_fetcher.filter_vacancies_by_keyword(salary_filtered_vacancies, keyword)

    # Проверка отфильтрованных вакансий
    if filtered_vacancies:
        print("Отфильтрованные вакансии:")
        print_vacancies(filtered_vacancies)
    else:
        print("Вакансий, соответствующих критериям, не найдено.")

    # Количество топ вакансий
    top_n_input = input("Введите количество топ вакансий для отображения: ")
    top_n = int(top_n_input) if top_n_input.isdigit() else None

    if top_n is not None:
        top_vacancies = Vacancy.get_top_vacancies(filtered_vacancies, top_n)
    else:
        top_vacancies = filtered_vacancies

    # Вывод результатов
    print("Топ вакансии:")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    main()
