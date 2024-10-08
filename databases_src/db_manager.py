import psycopg2


class DBManager:
    def __init__(self, db_name="kursovaya5", user="postgres", password="3219035", host="localhost", port="5432"):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def get_companies_and_vacancies_count(self):
        query = """
        SELECT companies.name, COUNT(vacancies.id) AS vacancy_count
        FROM companies
        LEFT JOIN vacancies ON companies.id = vacancies.company_id
        GROUP BY companies.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        query = """
        SELECT companies.name, vacancies.title, vacancies.salary, vacancies.url
        FROM vacancies
        JOIN companies ON vacancies.company_id = companies.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        query = """
        SELECT AVG(salary) FROM vacancies;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = """
        SELECT title, salary, url FROM vacancies
        WHERE salary > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        query = """
        SELECT title, salary, url FROM vacancies
        WHERE LOWER(title) LIKE %s;
        """
        self.cursor.execute(query, (f'%{keyword.lower()}%',))
        return self.cursor.fetchall()

    def save_company(self, company_name):
        query = """
        INSERT INTO companies (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        """
        self.cursor.execute(query, (company_name,))

    def save_vacancy(self, vacancy):
        query = """
        INSERT INTO vacancies (title, salary, url, company_id, description)
        VALUES (%s, %s, %s, (SELECT id FROM companies WHERE name = %s), %s)
        ON CONFLICT (url) DO NOTHING;
        """
        self.cursor.execute(query, (
            vacancy.title,
            vacancy.get_salary(),
            vacancy.url,
            vacancy.company_name,
            vacancy.description
        ))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db_manager = DBManager()
