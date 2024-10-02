from scr.api import HeadHunterAPI
from unittest.mock import patch


@patch('scr.api.requests.get')
def test_hh_api_get_vacancies(mock_get):
    mock_response = {
        "items": [
            {"name": "Python Developer", "url": "http://example.com/python-dev", "salary": {"from": 1500},
             "snippet": {"requirement": "Python, Django"}},
            {"name": "Java Developer", "url": "http://example.com/java-dev", "salary": {"from": 2000},
             "snippet": {"requirement": "Java, Spring"}}
        ]
    }
    mock_get.return_value.json.return_value = mock_response

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("developer")

    assert len(vacancies) == 2
    assert vacancies[0]['name'] == "Python Developer"
