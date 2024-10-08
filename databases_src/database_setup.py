import psycopg2


def create_tables():
    connection = psycopg2.connect(
        dbname='kursovaya5',
        user='postgres',
        password='3219035',
        host='localhost',
        port='5432'
    )

    cursor = connection.cursor()

    create_companies_table = """
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        description TEXT
    );
    """

    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        salary DECIMAL(10, 2),
        url VARCHAR(255) NOT NULL,
        company_id INTEGER REFERENCES companies(id),
        description TEXT
    );
    """

    cursor.execute(create_companies_table)
    cursor.execute(create_vacancies_table)

    # Уникальный индекс для вакансий
    create_unique_index = """
        CREATE UNIQUE INDEX IF NOT EXISTS unique_vacancy_url ON vacancies(url);
        """
    cursor.execute(create_unique_index)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_tables()
