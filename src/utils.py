import logging

import requests

from config import LOG_FORMAT, LOG_LEVEL
from src.api_hh import ApiHH
from src.db_manager import DBManager
from src.employer import Employer
from src.vacancy import Vacancy

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(LOG_FORMAT)
logger.addHandler(console_handler)
logger.setLevel(LOG_LEVEL)


def search_employers_on_hh(search_str: str) -> list:
    """
    Функция ищет компании по заданной строке на сайте HH.ru и выдает результат списком уникальных компаний
    :param search_str:
    :return список уникальных компаний:
    """
    api_hh = ApiHH()
    response = api_hh.load_vacancies(f"company_name:{search_str}")
    result = []
    list_id_for_check = []
    for i in range(len(response)):
        if not result or response[i].get("employer").get("id") not in list_id_for_check:
            result.append(Employer(response[i]))
            list_id_for_check.append(response[i].get("employer").get("id"))
    return result


def intro_employers_to_db_by_id(list_employer: list):
    """Функция получает список ID, и заносит в локальную базу этих работодателей и их вакансии"""
    vacancies = []
    for employer in list_employer:
        response = requests.get(f"https://api.hh.ru/vacancies?employer_id={employer}")
        vacancies.append(response.json()["items"])
    vacancies_list = []
    for vacancy in vacancies:
        for vacancy_data in vacancy:
            vacancies_list.append(Vacancy(vacancy_data))
    print("\nНайденные работодатели:")
    unique_employers = set()
    for vacancy in vacancies_list:
        unique_employers.add(vacancy.get_employer)
    for unique_employer in unique_employers:
        print(unique_employer)
    print()
    DBManager().vacancies = vacancies_list


def show_vacancies(vacancies_for_show: list, show_values):
    """Функция получает список вакансий для отображения на экране и отображает их согласно ограничению show_values
    После отработки, если ограничение show_values меняет свое значение - возвращает новое значение или старое.
    """
    for i in range(show_values if len(vacancies_for_show) > show_values else len(vacancies_for_show)):
        print(
            f"\nID: {vacancies_for_show[i][0]},\n"
            f"Вакансий: {vacancies_for_show[i][1]}\n"
            f"Зарплата от {vacancies_for_show[i][2]} до {vacancies_for_show[i][3]}\n"
            f"URL: {vacancies_for_show[i][4]}"
        )
    if len(vacancies_for_show) > show_values:
        print(
            f"\n1. Показать ВСЕ вакансии (найдено {len(vacancies_for_show)} "
            f"вакансий, показано {show_values})\n"
            f"9. Изменить кол-во значений для показа. (Установлено {show_values})\n"
            f"0. Вернуться в Меню Работы с Локальной БД"
        )
        value_menu_2_4 = input("введите пункт меню => ")
        match value_menu_2_4:
            case "1":
                for value in vacancies_for_show:
                    print()
                    print(
                        f"ID: {value[0]},\n"
                        f"Вакансий: {value[1]}\n"
                        f"Зарплата от {value[2]} до {value[3]}\n"
                        f"URL: {value[4]}"
                    )
            case "9":
                show_values = int(input("Введите количество значений для показа => "))
            case "0":
                pass
            case _:
                pass
    return show_values
