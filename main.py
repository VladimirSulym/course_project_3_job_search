import requests

from config import FAVORITES_EMPLOYERS
from src.db_init import logger
from src.db_manager import DBManager
from src.utils import (intro_employers_to_db_by_id, search_employers_on_hh,
                       show_vacancies)
from src.vacancy import Vacancy


def main():
    print("Добро пожаловать в Проект 3. Поиск вакансий с подключением БД.")
    value_menu = None
    show_values = 10
    db_manager = DBManager()
    skipping_menu_item = False
    full_show = False
    while value_menu != "0":
        if skipping_menu_item is False:
            print(
                f"\nГЛАВНОЕ МЕНЮ:\n"
                f"1. Найти работодателя и его вакансии по названию на НН.ru\n"
                f"2. Работа с локальной БД которая содержит:\n"
                f"   Вакансий {db_manager.count_vacancies}\n"
                f"   Компаний {db_manager.count_employers}\n"
                f"3. Ввести базу работодателей вручную.\n"
                f"9. Изменить кол-во значений для показа. (Установлено {show_values})\n"
                f"0. Выход"
            )
            value_menu = input("введите пункт меню => ")
        skipping_menu_item = False

        match value_menu:
            case "1":
                value_menu_1 = None
                user_input = input("Введите название компании для поиска => ")
                employers = search_employers_on_hh(user_input)
                if employers:
                    print(f"\nНайдено компаний: {len(employers)}\n")
                    for i in range(show_values if len(employers) > show_values else len(employers)):
                        print(employers[i])
                    while value_menu_1 != "0":
                        print("\nМЕНЮ РАБОТЫ С НАЙДЕННЫМИ КОМПАНИЯМИ:")
                        print("1. Сохранить найденных работодателей и их вакансии в локальной БД")
                        print("2. Показать вакансии выбранного работодателя")
                        print("3. Повторить поиск работодателя на сайте HH.ru")
                        if len(employers) > show_values and full_show is False:
                            print(
                                f"4. Показать ВСЕ компании (найдено {len(employers)} компаний, показано {show_values})"
                            )
                        full_show = False
                        print("0. Возврат в Главное Меню")
                        value_menu_1 = input("введите пункт меню => ")
                        match value_menu_1:
                            case "1":
                                db_manager.employers = employers
                                vacancies = []
                                try:
                                    for employer in employers:
                                        response = requests.get(employer.employer["vacancies_url"])
                                        vacancies_dict = response.json()["items"]
                                        for vacancy in vacancies_dict:
                                            vacancies.append(Vacancy(vacancy))
                                except Exception as e:
                                    logger.debug(e)
                                db_manager.vacancies = vacancies
                                DBManager()
                                value_menu_1 = "0"
                            case "2":
                                input_id_user = input("Введите ID работодателя => ")
                                print("")
                                for employer in employers:
                                    if input_id_user == employer.employer["id"]:
                                        response = requests.get(employer.employer["vacancies_url"])
                                        vacancies_2 = response.json()["items"]
                                        for vacancy in vacancies_2:
                                            print(Vacancy(vacancy))
                                value_menu_1_2 = None
                                while value_menu_1_2 != "0":
                                    print("1. Сохранить данного работодателя и его вакансии в локальной БД")
                                    print("0. Продолжить работу с ранее найденными работодателями")
                                    value_menu_1_2 = input("введите пункт меню => ")
                                    match value_menu_1_2:
                                        case "1":
                                            vacancies = []
                                            for vacancy in vacancies_2:
                                                vacancies.append(Vacancy(vacancy))
                                            db_manager.vacancies = vacancies
                                            DBManager()
                                            print("\nВсе данные успешно обработаны")
                                            value_menu_1_2 = "0"
                                            value_menu_1 = "0"
                                        case "0":
                                            pass
                                        case _:
                                            print("Нет такого пункта, повторите ввод")

                            case "3":
                                value_menu_1 = "0"
                                value_menu = "1"
                                skipping_menu_item = True
                            case "4":
                                for employer in employers:
                                    print(employer)
                                full_show = True
                            case "0":
                                pass
                            case _:
                                print("Нет такого пункта, повторите ввод")
                else:
                    print(f"Компания {user_input} не найдена на HH.ru")

            case "2":
                value_menu_2 = None
                while value_menu_2 != "0":
                    print("\nМЕНЮ РАБОТЫ С ЛОКАЛЬНОЙ БД:")
                    print(
                        "1. Показать список компаний и количество вакансий.\n"
                        "2. Показать список всех вакансий с указанием названия компании, "
                        "названия вакансии и зарплаты и ссылки на вакансию.\n"
                        "3. Показать среднюю зарплату по всем вакансиям.\n"
                        "4. Показать вакансий, у которых зарплата выше средней по всем вакансиям.\n"
                        "5. Найти вакансии по ключевому слову в названии"
                    )
                    print(
                        f"9. Изменить кол-во значений для показа. (Установлено {show_values})\n"
                        f"0. Вернуться в Главное Меню"
                    )
                    value_menu_2 = input("введите пункт меню => ")
                    match value_menu_2:
                        case "1":
                            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
                            print("")
                            if companies_and_vacancies_count:
                                for i in range(
                                    show_values
                                    if len(companies_and_vacancies_count) > show_values
                                    else len(companies_and_vacancies_count)
                                ):
                                    print(
                                        f"Компания: ID: {companies_and_vacancies_count[i][0]}, "
                                        f"Название: {companies_and_vacancies_count[i][1]}, содержит вакансий: "
                                        f"{companies_and_vacancies_count[i][2]}"
                                    )
                            if len(companies_and_vacancies_count) > show_values:
                                print(
                                    f"\n1. Показать ВСЕ компании (найдено {len(companies_and_vacancies_count)} "
                                    f"уникальных названий компаний, показано {show_values})\n"
                                    f"9. Изменить кол-во значений для показа. (Установлено {show_values})\n"
                                    f"0. Вернуться в Меню Работы с Локальной БД"
                                )
                                value_menu_2_1 = input("введите пункт меню => ")
                                match value_menu_2_1:
                                    case "1":
                                        for value in companies_and_vacancies_count:
                                            print(
                                                f"Компания: ID: {value[0]}, "
                                                f"Название: {value[1]}, "
                                                f"содержит вакансий: {value[2]}"
                                            )
                                    case "9":
                                        show_values = int(input("Введите количество значений для показа => "))
                                    case "0":
                                        pass
                                    case _:
                                        pass

                        case "2":
                            list_vacancies_found = db_manager.get_all_vacancies()
                            if list_vacancies_found:
                                print()
                                show_values = show_vacancies(list_vacancies_found, show_values)
                        case "3":
                            avg_salary = db_manager.get_avg_salary()
                            print("")
                            if avg_salary:
                                print(f"Средняя ЗП по всем вакансиям в локальной БД = {avg_salary}")
                        case "4":
                            vacancies_above_avg = db_manager.get_vacancies_with_higher_salary()
                            if vacancies_above_avg:
                                print()
                                show_values = show_vacancies(vacancies_above_avg, show_values)
                        case "5":
                            keyword = input("Введите ключевое слово для поиска => ")
                            vacancies_by_keyword = db_manager.get_vacancies_with_keyword(keyword)
                            if vacancies_by_keyword:
                                print()
                                show_values = show_vacancies(vacancies_by_keyword, show_values)
                            else:
                                print(f"Вакансий по запросу - {keyword} - не найдено.")
                        case "9":
                            show_values = int(input("Введите количество значений для показа => "))
                        case "0":
                            pass
                        case _:
                            print("Нет такого пункта, повторите ввод")
            case "3":
                print("1. Ввести ID работодателей через запятую\n" "2. Загрузить 10 избранных по умолчанию")
                value_menu_3 = input("введите пункт меню => ")
                match value_menu_3:
                    case "1":
                        list_employer = input("Введите ID работодателей через запятую => ").replace(" ", "").split(",")
                        intro_employers_to_db_by_id(list_employer)
                        DBManager()
                    case "2":
                        intro_employers_to_db_by_id(FAVORITES_EMPLOYERS)
                        DBManager()
            case "9":
                show_values = int(input("Введите количество значений для показа => "))
            case "0":
                pass
            case _:
                print("Нет такого пункта, повторите ввод")


if __name__ == "__main__":
    main()
