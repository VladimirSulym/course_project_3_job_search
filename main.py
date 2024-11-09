import requests

from src.api_hh import ApiHH
from src.db_manager import DBManager
from src.employer import Employer
from src.utils import search_employers_on_hh
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
            print(f'\nГЛАВНОЕ МЕНЮ:\n'
                  f'1. Найти работодателя на НН.ru\n'
                  f'2. Найти вакансию на НН.ru\n'
                  f'3. Работа с локальной БД которая содержит:\n'
                  f'   Вакансий {db_manager.count_vacancies}\n'
                  f'   Компаний {db_manager.count_employers}\n'
                  f'9. Изменить кол-во значений для показа. (Установлено {show_values})\n'
                  f'0. Выход')
            value_menu = input('введите пункт меню => ')
        skipping_menu_item = False

        match value_menu:
            case "1":
                value_menu_1 = None
                user_input = input('Введите название компании для поиска => ')
                employers = search_employers_on_hh(user_input)
                if employers:
                    print(f'\nНайдено компаний: {len(employers)}\n')
                    for i in range(show_values if len(employers) > show_values else len(employers)):
                        print(employers[i])
                    while value_menu_1 != "0":
                        print(f'\nМЕНЮ РАБОТЫ С НАЙДЕННЫМИ КОМПАНИЯМИ:')
                        print('1. Сохранить найденных работодателей в локальной БД')
                        print('2. Показать вакансии выбранного работодателя')
                        print('3. Повторить поиск работодателя на сайте HH.ru')
                        if len(employers) > show_values and full_show is False:
                            print(f'4. Показать ВСЕ компании (найдено {len(employers)} компаний, показано {show_values})')
                        full_show = False
                        print('0. Возврат в Главное Меню')
                        value_menu_1 = input('введите пункт меню => ')
                        match value_menu_1:
                            case "1":
                                db_manager.employers = employers
                                DBManager()
                            case "2":
                                input_id_user = input("Введите ID работодателя => ")
                                print('')
                                for employer in employers:
                                    if input_id_user == employer.employer['id']:
                                        response = requests.get(employer.employer['vacancies_url'])
                                        vacancies = response.json()["items"]
                                        for vacancy in vacancies:
                                            print(Vacancy(vacancy))

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
                    print(f'Компания {user_input} не найдена на HH.ru')

            case "2":
                pass
            case "3":
                value_menu_3 = None
                while value_menu_3 != "0":
                    print("\nМЕНЮ РАБОТЫ С ЛОКАЛЬНОЙ БД:")
                    print(f'1. Показать список компаний и количество вакансий.\n'
                          f'2. Показать список всех вакансий с указанием названия компании, '
                          f'названия вакансии и зарплаты и ссылки на вакансию.\n'
                          f'3. Показать среднюю зарплату по всем вакансиям.\n'
                          f'4. Показать вакансий, у которых зарплата выше средней по всем вакансиям.\n'
                          f'5. Найти вакансии по ключевому слову в названии')
                    print(f'9. Изменить кол-во значений для показа. (Установлено {show_values})\n'
                          f'0. Вернуться в Главное Меню')
                    value_menu_3 = input('введите пункт меню => ')
                    match value_menu_3:
                        case "1":
                            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
                            print('')
                            if companies_and_vacancies_count:
                                for i in range(show_values if len(companies_and_vacancies_count) > show_values else len(
                                        companies_and_vacancies_count)):
                                    print(
                                        f'Компания: {companies_and_vacancies_count[i][0]}, содержит вакансий: '
                                        f'{companies_and_vacancies_count[i][1]}')
                            if len(companies_and_vacancies_count) > show_values:
                                print(f'\n1. Показать ВСЕ компании (найдено {len(companies_and_vacancies_count)} '
                                      f'уникальных названий компаний, показано {show_values})\n'
                                      f'9. Изменить кол-во значений для показа. (Установлено {show_values})\n'
                                      f'0. Вернуться в Меню Работы с Локальной БД')
                                value_menu_3_1 = input('введите пункт меню => ')
                                match value_menu_3_1:
                                    case "1":
                                        for value in companies_and_vacancies_count:
                                            print(f'Компания: {value[0]}, содержит вакансий: {value[1]}')
                                    case "9":
                                        show_values = int(input('Введите количество значений для показа => '))
                                    case "0":
                                        pass
                                    case _:
                                        pass

                        case "2":
                            list_vacancies_found = db_manager.get_all_vacancies()
                            print('')
                            if list_vacancies_found:
                                for i in range(show_values if len(list_vacancies_found) > show_values else len(
                                        list_vacancies_found)):
                                    print(
                                        f'\nКомпания: {list_vacancies_found[i][0]},\n'
                                        f'Вакансий: {list_vacancies_found[i][1]}\n'
                                        f'Зарплата от {list_vacancies_found[i][2]} до {list_vacancies_found[i][3]}\n'
                                        f'URL: {list_vacancies_found[i][4]}')
                                if len(list_vacancies_found) > show_values:
                                    print(f'\n1. Показать ВСЕ вакансии (найдено {len(list_vacancies_found)} '
                                          f'вакансий, показано {show_values})\n'
                                          f'9. Изменить кол-во значений для показа. (Установлено {show_values})\n'
                                          f'0. Вернуться в Меню Работы с Локальной БД')
                                    value_menu_3_2 = input('введите пункт меню => ')
                                    match value_menu_3_2:
                                        case "1":
                                            for value in list_vacancies_found:
                                                print(
                                                    f'Компания: {value[0]},\n'
                                                    f'Вакансий: {value[1]}\n'
                                                    f'Зарплата от {value[2]} до {value[3]}\n'
                                                    f'URL: {value[4]}')
                                        case "9":
                                            show_values = int(input('Введите количество значений для показа => '))
                                        case "0":
                                            pass
                                        case _:
                                            pass
                        case "3":
                            avg_salary = db_manager.get_avg_salary()
                            print('')
                            if avg_salary:
                                print(f'Средняя ЗП по всем вакансиям в локальной БД = {avg_salary}')
                        case "4":
                            vacancies_above_avg = db_manager.get_vacancies_with_higher_salary()
                            print('')
                            if vacancies_above_avg:
                                print()
                                for i in range(show_values if len(vacancies_above_avg) > show_values else len(
                                        vacancies_above_avg)):
                                    print(
                                        f'\nID: {vacancies_above_avg[i][0]},\n'
                                        f'Вакансий: {vacancies_above_avg[i][1]}\n'
                                        f'Зарплата от {vacancies_above_avg[i][2]} до {vacancies_above_avg[i][3]}\n'
                                        f'URL: {vacancies_above_avg[i][4]}')
                                if len(vacancies_above_avg) > show_values:
                                    print(f'\n1. Показать ВСЕ вакансии (найдено {len(vacancies_above_avg)} '
                                          f'вакансий, показано {show_values})\n'
                                          f'9. Изменить кол-во значений для показа. (Установлено {show_values})\n'
                                          f'0. Вернуться в Меню Работы с Локальной БД')
                                    value_menu_3_4 = input('введите пункт меню => ')
                                    match value_menu_3_4:
                                        case "1":
                                            for value in vacancies_above_avg:
                                                print(
                                                    f'ID: {value[0]},\n'
                                                    f'Вакансий: {value[1]}\n'
                                                    f'Зарплата от {value[2]} до {value[3]}\n'
                                                    f'URL: {value[4]}')
                                        case "9":
                                            show_values = int(input('Введите количество значений для показа => '))
                                        case "0":
                                            pass
                                        case _:
                                            pass
                        case "5":
                            keyword = input('Введиет ключевое слово для поиска => ')
                            vacancies_by_keyword = db_manager.get_vacancies_with_keyword(keyword)
                            print('')
                            if vacancies_by_keyword:
                                for i in range(show_values if len(vacancies_by_keyword) > show_values else len(
                                        vacancies_by_keyword)):
                                    print(
                                        f'\nID: {vacancies_by_keyword[i][0]},\n'
                                        f'Вакансий: {vacancies_by_keyword[i][1]}\n'
                                        f'Зарплата от {vacancies_by_keyword[i][2]} до {vacancies_by_keyword[i][3]}\n'
                                        f'URL: {vacancies_by_keyword[i][4]}')
                                if len(vacancies_by_keyword) > show_values:
                                    print(f'\n1. Показать ВСЕ вакансии (найдено {len(vacancies_by_keyword)} '
                                          f'вакансий, показано {show_values})\n'
                                          f'9. Изменить кол-во значений для показа. (Установлено {show_values})\n'
                                          f'0. Вернуться в Меню Работы с Локальной БД')
                                    value_menu_3_5 = input('введите пункт меню => ')
                                    match value_menu_3_5:
                                        case "1":
                                            for value in vacancies_by_keyword:
                                                print(
                                                    f'ID: {value[0]},\n'
                                                    f'Вакансий: {value[1]}\n'
                                                    f'Зарплата от {value[2]} до {value[3]}\n'
                                                    f'URL: {value[4]}')
                                        case "9":
                                            show_values = int(input('Введите количество значений для показа => '))
                                        case "0":
                                            pass
                                        case _:
                                            pass
                            else:
                                print(f'Вакансий по запросу - {keyword} - не найдено.')
                        case "9":
                            show_values = int(input('Введите количество значений для показа => '))
                        case "0":
                            pass
                        case _:
                            print("Нет такого пункта, повторите ввод")
            case "9":
                show_values = int(input('Введите количество значений для показа => '))
            case "0":
                pass
            case _:
                print("Нет такого пункта, повторите ввод")


if __name__ == '__main__':
    main()
    #
    # api_hh = ApiHH()
    # # result = api_hh.load_vacancies('name:(продажи or Менеджер) and company_name:РДЭ')
    # result = api_hh.load_vacancies('инженер')
    # vacancies = []
    # for i in range(len(result)):
    #     vacancies.append(Vacancy(result[i]))
    # print(vacancies[0])
    # DBManager().vacancies = vacancies

    # temp1 = Vacancy(result[0])
    # print(temp1)

    # for i in range(4):
    #     pass
    #     # print(result[i])
    #     print(result[i]['employer']['name'])
    #     print(result[i]['name'])
    # request = requests.get(result[1]['employer']['vacancies_url'])
    # request = requests.get('https://api.hh.ru/vacancies?employer_id=604039')
    # print(request.json()['items'][0])
