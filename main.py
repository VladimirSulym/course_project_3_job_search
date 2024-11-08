from src.api_hh import ApiHH
from src.db_manager import DBManager
from src.employer import Employer
from src.utils import search_employers_on_hh
from src.vacancy import Vacancy

def main():
    print ("Добро пожаловать в Проект 3. Поиск вакансий с подключением БД.")
    value_menu = None
    show_values = 10
    while value_menu != "0":
        print(f'\nГЛАВНОЕ МЕНЮ:\n'
              f'1. Найти работодателя на НН.ru\n'
              f'2. Найти вакансию на НН.ru\n'
              f'3. Работа с локальной БД которая содержит:\n'
              f'   Вакансий {10}\n'
              f'   Компаний {10}\n'
              f'9. Изменить кол-во значений для показа. Установлено {show_values}\n'
              f'0. Выход')
        value_menu = input('введите пункт меню => ')

        match value_menu:
            case "1":
                value_menu_1 = None
                overflow_show = False
                user_input = input('Введите название компании для поиска => ')
                print('')
                employers = search_employers_on_hh(user_input)
                if employers:
                    print(f'Найдено компаний: {len(employers)}')
                    for i in range(show_values if len(employers) > show_values else len(employers)):
                        print(employers[i])
                else:
                    print(f'Компания {user_input} не найдена на HH.ru')
                while value_menu_1 != "0":
                    print(f'\nМЕНЮ РАБОТЫ С НАЙДЕННЫМИ КОМПАНИЯМИ:')
                    print('1. Сохранить найденных работодателей в локальной БД')
                    print('2. Показать вакансии выбранного работодателя')
                    print('3. Повторить поиск работодателя на сайте HH.ru')
                    if len(employers) > show_values:
                        print(f'4. Показать ВСЕ компании (найдено {len(employers)}, показано {show_values})')
                    print('0. Возврат в Главное Меню')
                    value_menu_1 = input('введите пункт меню => ')
                    match value_menu_1:
                        case "1":
                            pass
                        case "2":
                            pass
                        case "3":
                            pass
                        case "0":
                            pass
                        case _:
                            print("Нет такого пункта, повторите ввод")

            case "2":
                pass
            case "3":
                pass
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