from databases_src.db_manager import DBManager


def test_db_manager():
    db_manager = DBManager(db_name="kursovaya5", user="postgres", password="3219035")

    # Получаем компании и вакансии
    companies = db_manager.get_companies_and_vacancies_count()
    print("Компании и количество вакансий:")
    for company in companies:
        print(company)

    # Получаем все вакансии
    vacancies = db_manager.get_all_vacancies()
    print("\nВсе вакансии:")
    for vacancy in vacancies:
        print(vacancy)

    # Средняя зарплата
    avg_salary = db_manager.get_avg_salary()
    print(f"\nСредняя зарплата: {avg_salary}")

    # Вакансии с зарплатой выше средней
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print("\nВакансии с зарплатой выше средней:")
    for vacancy in high_salary_vacancies:
        print(vacancy)

    # Вакансии по ключевому слову
    keyword = "Python"
    keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    print(f"\nВакансии по ключевому слову '{keyword}':")
    for vacancy in keyword_vacancies:
        print(vacancy)

    db_manager.close()


if __name__ == "__main__":
    test_db_manager()
