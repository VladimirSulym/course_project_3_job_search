class Employer:
    def __init__(self, data):
        self.employer = {
            "id": data.get("id"),
            "name": data.get("name"),
            "url": data.get("alternate_url"),
            "vacancies_url": data.get("vacancies_url"),
        }

    def __str__(self):
        return (
            f'ID: {self.employer.get("id")}\n'
            f'Работодатель: {self.employer.get("name")}\n'
            f"Ссылка: {self.employer.get('url')}\n"
            f"Ссылка на вакансии: {self.employer.get('vacancies_url')}"
        )