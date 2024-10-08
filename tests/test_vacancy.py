from src.vacancy import Vacancy


def test_vacancy_creation():
    """Тест создания объекта вакансии"""
    vacancy = Vacancy(
        title="Python Developer",
        url="http://example.com/python-developer",
        salary=2000,
        description="Great Python job"
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.salary == 2000


def test_vacancy_filter_by_keyword():
    """Тест фильтрации вакансий по ключевому слову"""
    vacancy1 = Vacancy(title="Python Developer", url="http://example.com/python-developer", salary=2000, description="Python job")
    vacancy2 = Vacancy(title="Java Developer", url="http://example.com/java-developer", salary=2500, description="Java job")

    vacancies = [vacancy1, vacancy2]

    filtered = [vac for vac in vacancies if 'Python' in vac.description]

    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"


def test_vacancy_salary_filter():
    """Тест фильтрации вакансий по зарплате"""
    vacancy1 = Vacancy(title="Python Developer", url="http://example.com/python-developer", salary=2000, description="Python job")
    vacancy2 = Vacancy(title="Junior Developer", url="http://example.com/junior-developer", salary=1000, description="Entry level job")

    vacancies = [vacancy1, vacancy2]

    filtered = [vac for vac in vacancies if vac.salary >= 1500]

    assert len(filtered) == 1
    assert filtered[0].title == "Python Developer"
