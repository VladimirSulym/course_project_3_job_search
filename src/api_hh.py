import requests
import logging

from config import LOG_FORMAT, LOG_LEVEL

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(LOG_FORMAT)
logger.addHandler(console_handler)
logger.setLevel(LOG_LEVEL)

class ApiHH:
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        self.vacancies_cont = 0

    def __api_connection(self):
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        logger.debug(f"Статус код - {response.status_code}")
        logger.debug(f"Количество найденных вакансий {response.json()['found']}")
        return response

    def load_vacancies(self, keyword: str) -> list:
        """Функция получает на вход слово для поиска на сайте hh и список словарей с вакансиями"""
        self.__params["text"] = keyword
        pages_count = 20
        while self.__params.get("page") < pages_count:
            response = self.__api_connection()
            self.vacancies_cont = response.json()["found"]
            if response.json()["pages"] < pages_count:
                logger.debug(f"Кол-во страниц {response.json()['pages']} - меньше 20")
                pages_count = response.json()["pages"]
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1
        return self.__vacancies
