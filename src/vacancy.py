class Vacancy:
    def __init__(self, title, url, salary, description, company_name):
        self.title = title
        self.url = url
        self.salary = salary if salary else "Зарплата не указана"
        self.description = description
        self.company_name = company_name
        self.validate()

    def __lt__(self, other):
        return self.get_salary() < other.get_salary()

    def _get_salary_from_str(self):
        """Извлекает минимальную зарплату, возвращает как целое число"""
        if isinstance(self.salary, dict):
            # Предположим, что 'from' — это минимальная зарплата
            return int(self.salary.get("from", 0) or 0)
        elif isinstance(self.salary, str):
            # Проверка зарплаты
            if "не указана" in self.salary:
                return 0
            min_salary_str = self.salary.split("–")[0].strip()
            return int(min_salary_str.replace(" ", "").replace("руб.", "").replace("руб", ""))
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

    @classmethod
    def cast_to_object_list(cls, vacancies):
        """Преобразует список словарей в список объектов Vacancy"""
        vacancies_list = []
        for vacancy in vacancies:
            if isinstance(vacancy, dict):
                title = vacancy.get("name")
                url = vacancy.get("alternate_url")
                salary = vacancy.get("salary")
                description = vacancy.get("snippet", {}).get("responsibility", "")
                company_name = vacancy.get('employer', {}).get('name')
                vacancies_list.append(cls(title, url, salary, description, company_name))
            else:
                print(f"Неправильный формат данных: {vacancy}")
        return vacancies_list

    @staticmethod
    def get_top_vacancies(vacancies, n):
        """Возвращает топ N вакансий по зарплате"""
        sorted_vacancies = sorted(vacancies, key=lambda v: v.get_salary(),
                                  reverse=True)
        return sorted_vacancies[:n]

