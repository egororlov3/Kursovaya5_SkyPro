import json
import os


class JSONSaver:
    def __init__(self, filename='data/vacancies.json'):
        self.filename = filename
        self.load_existing_vacancies()

    def load_existing_vacancies(self):
        """Загружает существующие вакансии из файла"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.existing_vacancies = json.load(file)
        else:
            self.existing_vacancies = []

    def add_vacancy(self, vacancy):
        """Добавляет вакансию в файл, если её там еще нет"""
        if vacancy.url not in [v['url'] for v in self.existing_vacancies]:
            self.existing_vacancies.append({
                'title': vacancy.title,
                'url': vacancy.url,
                'salary': vacancy.salary,
                'description': vacancy.description,
            })
            self.save_to_file()  # Сохранение после добавления

    def save_to_file(self):
        """Сохраняет все вакансии в файл"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.existing_vacancies, file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy):
        """Удаляет вакансию из файла, если она там есть"""
        self.existing_vacancies = [v for v in self.existing_vacancies if v['url'] != vacancy.url]
        self.save_to_file()  # Сохранение после удаления
