from src.api_hh import ApiHH

import logging

from config import LOG_FORMAT, LOG_LEVEL
from src.employer import Employer

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
    response = api_hh.load_vacancies(f'company_name:{search_str}')
    result = []
    list_id_for_check = []
    for i in range(len(response)):
        if not result or response[i].get('employer').get('id') not in list_id_for_check:
            result.append(Employer(response[i]))
            list_id_for_check.append(response[i].get('employer').get('id'))
    return result