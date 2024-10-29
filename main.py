import requests

from src.api_hh import ApiHH

if __name__ == '__main__':
    api_hh = ApiHH()
    result = api_hh.load_vacancies('name:(продажи or Менеджер) and company_name:РДЭ')
    for i in range(1):
        pass
        print(result[i])
        # print(result[i]['employer']['name'])
        # print(result[i]['name'])
    request = requests.get(result[1]['employer']['vacancies_url'])
    # request = requests.get('https://api.hh.ru/vacancies?employer_id=604039')
    print(request.json()['items'][0])