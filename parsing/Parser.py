from abc import ABC, abstractmethod
from typing import TypeVar

import bs4
import requests

from bs4 import BeautifulSoup

HH_URL = 'https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python&excluded_text=&area=113&area=40&area=16&area=1001&salary=&currency_code=RUR&experience=noExperience&schedule=fullDay&schedule=remote&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=vacancy_search_filter'
# SJ_URL = 'https://spb.superjob.ru/vacancy/search/?keywords=Python'
HC_URL = 'https://career.habr.com/vacancies?q=python&type=all'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
}


class JobCard(ABC):
    job_card_type = TypeVar('job_card_type', bound='JobCard')

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def title_url(self):
        pass

    @property
    @abstractmethod
    def city(self):
        pass

    def __init__(self, tag: bs4.Tag):
        self.tag = tag

    def get_title(self):
        return self.tag.select_one(self.title).text

    def get_url(self):
        return self.tag.select_one(self.title_url).attrs.get('href')

    def get_city(self):
        return self.tag.select_one(self.city).text


class Page(ABC):
    @property
    @abstractmethod
    def card_class(self):
        pass

    @property
    @abstractmethod
    def card(self):
        pass

    def __init__(self, url: str):
        self.url = url

        self._bs_page = None

    def parser(self):
        result = requests.get(self.url, headers=HEADERS)

        self._bs_page = BeautifulSoup(result.text, 'lxml')

    def get_list_vacancies(self) -> list:
        vacs = self._bs_page.select(self.card)

        cards = [self.card_class(tag) for tag in vacs]
        names = [(card.get_title(), card.get_city(), card.get_url()) for card in cards]
        return names


class HHJobCard(JobCard):
    title = '[data-qa="serp-item__title"]'
    title_url = '[class="bloko-link"]'
    city = '[data-qa="vacancy-serp__vacancy-address_narrow"]'


class HHPage(Page):
    card_class = HHJobCard
    card = '[data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus"]'


# class SJJobCard(JobCard):
#     title = 'span a[href]'
#     title_url = title
#     city = 'div > span'
#
#     def get_title(self):
#         return self.tag.select_one(self.title).text
#
#     def get_url(self):
#         return self.tag.select_one(self.title_url).attrs.get('href')
#
#     def get_city(self):
#         return self.tag.select(self.city)[6].text
#
#
# class SJPage(Page):
#     card_class = SJJobCard
#     card = '[class=f-test-vacancy-item"]'


class HabrJobCard(JobCard):
    title = '[class="vacancy-card__title-link"]'
    title_url = title
    city = '[class="link-comp link-comp--appearance-dark"]'


class HabrPage(Page):
    card = '[class="vacancy-card"]'
    card_class = HabrJobCard


if __name__ == '__main__':
    page = HHPage(HH_URL)
    page.parser()
    print(*page.get_list_vacancies(), sep='\n')
