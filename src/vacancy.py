from src.employer import Employer


class Vacancy:
    """Класс для хранения данных о вакансии"""

    __slots__ = "vacancy", "employer"

    def __init__(self, data: dict):
        self.vacancy = {
            "id": data.get("id"),
            "name": data.get("name"),
            "employer_id": data.get("employer").get("id"),
            "area": "",
            "salary_from": 0,
            "salary_to": 0,
            "currency": "",
            "url": data.get("alternate_url"),
            "requirement": data.get("snippet").get("requirement"),
            "responsibility": data.get("snippet").get("responsibility"),
            "schedule": "",
        }
        self.employer = Employer(data)
        self.__data_validation(data)

    @property
    def get_vacancy(self):
        return self.vacancy.get("name")

    @property
    def get_employer(self):
        return self.employer.get_employer

    def __data_validation(self, data: dict) -> None:
        if data.get("salary"):
            if data.get("salary").get("from"):
                self.vacancy["salary_from"] = data.get("salary").get("from")
            else:
                self.vacancy["salary_from"] = 0
            if data.get("salary").get("to"):
                self.vacancy["salary_to"] = data.get("salary").get("to")
            else:
                self.vacancy["salary_to"] = 0
            if data.get("salary").get("currency"):
                self.vacancy["currency"] = data.get("salary").get("currency")
            else:
                self.vacancy["currency"] = ""
            # self.vacancy["salary"]["currency"] = data.get("salary").get("currency")
            # self.vacancy["salary"]["gross"] = data.get("salary").get("gross")
        if type(data.get("area")) == dict:
            self.vacancy["area"] = data.get("area").get("name")
        else:
            self.vacancy["area"] = data.get("area")
        if type(data.get("schedule")) == dict:
            self.vacancy["schedule"] = data.get("schedule").get("name")
        else:
            self.vacancy["schedule"] = data.get("schedule")

    def __str__(self):
        return (
            f'ID: {self.vacancy.get("id")}\n'
            f'Название: {self.vacancy.get("name")}\n'
            f'Работодатель: {self.employer.employer["name"]}\n'
            f'Регион: {self.vacancy.get("area")}\n'
            f"Зарплата от: {self.vacancy.get('salary_from')}, до: {self.vacancy.get('salary_to')} "
            f"{self.vacancy.get('currency')}\n"
            f"Ссылка на вакансию: {self.vacancy.get('url')}\n"
            f"Описание:\n"
            f"Требования: {self.vacancy.get('requirement')}\n"
            f"Обязанности: {self.vacancy.get('responsibility')}\n"
        )

    def __lt__(self, other):
        return self.vacancy.get("salary_from") < other.vacancy.get("salary_from")

    def __gt__(self, other):
        return self.vacancy.get("salary_from") > other.vacancy.get("salary_from")
