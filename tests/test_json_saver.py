import pytest
import json
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def vacancy():
    """Фикстура для создания тестовой вакансии"""
    return Vacancy(
        title="Test Vacancy",
        url="http://example.com/test-vacancy",
        salary=1000,
        description="Test description"
    )


@pytest.fixture
def json_saver(tmpdir):
    """Фикстура для создания временного JSON-файла"""
    temp_file = tmpdir.join('vacancies.json')
    return JSONSaver(filename=str(temp_file))


def test_add_vacancy(json_saver, vacancy):
    """Тест добавления вакансии в JSON-файл"""
    json_saver.add_vacancy(vacancy)
    assert len(json_saver.existing_vacancies) == 1
    assert json_saver.existing_vacancies[0]['title'] == "Test Vacancy"


def test_duplicate_vacancy(json_saver, vacancy):
    """Тест предотвращения дублирования вакансий"""
    json_saver.add_vacancy(vacancy)
    json_saver.add_vacancy(vacancy)  # Добавляем ту же вакансию второй раз
    assert len(json_saver.existing_vacancies) == 1  # Дубликат не должен добавиться


def test_delete_vacancy(json_saver, vacancy):
    """Тест удаления вакансии из JSON-файла"""
    json_saver.add_vacancy(vacancy)
    assert len(json_saver.existing_vacancies) == 1
    json_saver.delete_vacancy(vacancy)
    assert len(json_saver.existing_vacancies) == 0


def test_save_to_file(json_saver, vacancy):
    """Тест сохранения вакансий в файл"""
    json_saver.add_vacancy(vacancy)
    json_saver.save_to_file()

    with open(json_saver.filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]['title'] == "Test Vacancy"
