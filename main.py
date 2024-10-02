from scr.api import HeadHunterAPI
from scr.vacancy import Vacancy
from scr.json_saver import JSONSaver


def user_interaction():
    search_query = input("Введите поисковый запрос для вакансий: ")
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(vacancies)

    json_saver = JSONSaver()

    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)  # Сохранение каждой вакансии в JSON

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_vacancies = Vacancy.get_top_vacancies(vacancies_list, top_n)
    print("\nТоп вакансий по зарплате:")
    print_vacancies(top_vacancies)

    filter_keyword = input("Введите ключевое слово для фильтрации вакансий: ")
    filtered_vacancies = [
        vacancy for vacancy in vacancies_list
        if vacancy.description and filter_keyword.lower() in vacancy.description.lower()
    ]

    print(f"\nВсего вакансий после фильтрации по ключевому слову '{filter_keyword}': {len(filtered_vacancies)}")

    min_salary_input = input("Введите минимальную зарплату (или оставьте пустым для пропуска): ")
    max_salary_input = input("Введите максимальную зарплату (или оставьте пустым для пропуска): ")

    min_salary = int(min_salary_input) if min_salary_input else None
    max_salary = int(max_salary_input) if max_salary_input else None

    salary_filtered_vacancies = []
    for vacancy in filtered_vacancies:
        salary = vacancy.get_salary()
        if (min_salary is None or salary >= min_salary) and (max_salary is None or salary <= max_salary):
            salary_filtered_vacancies.append(vacancy)

    print("\nОтфильтрованные вакансии по зарплате:")
    print_vacancies(salary_filtered_vacancies)


def print_vacancies(vacancies):
    if not vacancies:
        print("Нет доступных вакансий")
        return

    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}\n")


if __name__ == "__main__":
    user_interaction()
