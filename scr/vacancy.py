class Vacancy:
    def __init__(self, title, url, salary, description):
        self.title = title
        self.url = url
        self.salary = salary if salary else "Зарплата не указана"
        self.description = description
        self.validate()

    def __lt__(self, other):
        return self.get_salary() < other.get_salary()

    def _get_salary_from_str(self):
        """Извлекает минимальную зарплату и возвращает как целое число"""
        if isinstance(self.salary, dict):
            return self.salary.get("from") or 0
        elif isinstance(self.salary, str) and "–" in self.salary:
            min_salary = self.salary.split("–")[0].strip()
            return int(min_salary.replace(" ", "").replace("руб.", ""))
        elif isinstance(self.salary, int):
            return self.salary
        return 0

    def get_salary(self):
        """Возвращает минимальную зарплату"""
        return self._get_salary_from_str()

    def validate(self):
        """Валидация данных"""
        if not self.title or not self.url:
            raise ValueError("Название и ссылка на вакансию обязательны.")

    def __repr__(self):
        return f"{self.title} ({self.salary}) - {self.url}"

    @staticmethod
    def cast_to_object_list(vacancies_data):
        vacancies = []
        for data in vacancies_data:
            if isinstance(data, dict):
                title = data.get("name")
                url = data.get("alternate_url")
                salary = data.get("salary")
                description = data.get("snippet", {}).get("responsibility", "")
                print(f"Создаем вакансию: {title}")
                vacancies.append(Vacancy(title, url, salary, description))
            else:
                print(f"Неправильный формат данных: {data}")
        return vacancies

    @staticmethod
    def get_top_vacancies(vacancies, n):
        """Возвращает топ N вакансий по зарплате"""
        sorted_vacancies = sorted(vacancies, key=lambda v: v.get_salary(),
                                  reverse=True)
        return sorted_vacancies[:n]

