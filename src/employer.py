class Employer:
    """Класс для хранения данных о работодателе"""

    def __init__(self, data):
        self.employer = {
            "id": data.get("employer").get("id"),
            "name": data.get("employer").get("name"),
            "url": data.get("employer").get("alternate_url"),
            "vacancies_url": data.get("employer").get("vacancies_url"),
        }

    def __str__(self):
        return (
            f'ID: {self.employer.get("id")}\n'
            f'Работодатель: {self.employer.get("name")}\n'
            f"Ссылка: {self.employer.get('url')}\n"
            f"Ссылка на вакансии: {self.employer.get('vacancies_url')}"
        )

    @property
    def get_employer(self):
        return self.employer.get("name")
