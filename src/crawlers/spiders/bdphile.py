import string
from typing import Any, Dict, Optional

import scrapy
from scrapy.selector import Selector

from crawlers.items import AuthorsItem
from utils.html import clean_html_text
from utils.log import get_log

logger = get_log(__file__)

LETTER_FILTERS = string.ascii_uppercase + "*"


class BaseBdphileSpider(scrapy.Spider):
    allowed_domains = ["bdphile.fr"]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def start_requests(self):
        start_url = self.start_urls[0]
        for letter in LETTER_FILTERS:
            yield scrapy.Request(url=start_url.format(letter), callback=self.parse)

    def _parse_link(self):
        raise NotImplementedError

    def parse(self, response: scrapy.http.Response):
        main_div = response.xpath(
            "//div[contains(concat(' ', normalize-space(@class), ' '), ' col-lg-6 ')]"
        ).get()
        links_tag = Selector(text=main_div).xpath("//a")
        logger.info(len(links_tag))
        for link_tag in links_tag:
            link = link_tag.xpath("@href")
            yield scrapy.Request(url=link.get(), callback=self._parse_link)


class BdphileSpider(scrapy.Spider):
    name = "bdphile_authors"
    start_urls = [
        "https://www.bdphile.fr/author/?filters%5Bletter%5D={}&filters%5Brole%5D=&filters%5Bnationality%5D="
    ]
    allowed_domains = ["bdphile.fr"]

    def start_requests(self):
        start_url = self.start_urls[0]
        for letter in LETTER_FILTERS:
            yield scrapy.Request(url=start_url.format(letter), callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        main_div = response.xpath(
            "//div[contains(concat(' ', normalize-space(@class), ' '), ' col-lg-6 ')]"
        ).get()
        links_tag = Selector(text=main_div).xpath("//a")
        logger.info(len(links_tag))
        for link_tag in links_tag:
            link = link_tag.xpath("@href")
            yield scrapy.Request(url=link.get(), callback=self._parse_link)

    def _parse_link(self, response: scrapy.http.Response):
        logger.info(f"Visiting author page {response.url}")

        names = response.css("h1 *::text").getall()
        nick_name = ""
        full_name = ""
        for name in names:
            cleaned_name = clean_html_text(name)

            if "(" in cleaned_name and ")" in cleaned_name:
                start = cleaned_name.index("(")
                end = cleaned_name.index(")")
                nick_name = cleaned_name[start + 1 : end]
            elif "(" not in cleaned_name and ")" not in cleaned_name and cleaned_name:
                full_name = cleaned_name

        first_name, *last_name = full_name.split(" ")
        last_name = " ".join(last_name)

        activity = response.css("h2 *::text").get()
        activity = "" if activity == "Dernières sorties" else activity

        yield scrapy.Request(
            url=response.url.replace("view", "bio"),
            callback=self.parse_author_bio,
            cb_kwargs={
                "author": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "nick_name": nick_name,
                    "activity": activity,
                }
            },
        )

    def parse_author_bio(self, response: scrapy.http.Response, author: Dict[str, str]):
        bio_div = response.css("div.postbody *::text").extract()
        bio, is_valid_bio = "", True
        for text in bio_div:
            if "la biographie de cet auteur est vide." in clean_html_text(text).lower():
                is_valid_bio = False

        if is_valid_bio:
            bio = " ".join([text for text in bio_div if clean_html_text(text)])

        author["biography"] = bio

        yield AuthorsItem(**author)


class BdphileSpider(BaseBdphileSpider):
    name = "bdphile_series"
    start_urls = [
        "https://www.bdphile.fr/series/?order=%60list_name%60+ASC&filters%5Bletter%5D={}&filters%5Btype%5D=&filters%5Bgenre%5D=&filters%5Bstatus%5D="
    ]

    def start_requests(self):
        start_url = self.start_urls[0]
        for letter in "a":
            yield scrapy.Request(
                url=start_url.format(letter), callback=self.parse_pages
            )

    def parse_pages(self, response: scrapy.http.Response):
        pages = response.css("div .pages").get()
        logger.info(pages)
        links_tag = Selector(text=main_div).xpath("//a")
        logger.info(len(links_tag))
        for link_tag in links_tag:
            link = link_tag.xpath("@href")
            yield scrapy.Request(url=link.get(), callback=self._parse_link)

    def parse(self, response: scrapy.http.Response):
        main_div = response.xpath(
            "//div[contains(concat(' ', normalize-space(@class), ' '), ' col-lg-6 ')]"
        ).get()
        links_tag = Selector(text=main_div).xpath("//a")
        logger.info(len(links_tag))
        for link_tag in links_tag:
            link = link_tag.xpath("@href")
            yield scrapy.Request(url=link.get(), callback=self._parse_link)

    def _parse_link(self, response: scrapy.http.Response):
        logger.info(f"Visiting serie page {response.url}")

        # yield scrapy.Request(
        #     url=response.url.replace("view", "bio"),
        #     callback=self.parse_author_bio,
        #     cb_kwargs={
        #         "author": {
        #             "first_name": first_name,
        #             "last_name": last_name,
        #             "nick_name": nick_name,
        #             "activity": activity,
        #         }
        #     },
        # )

    def parse_author_bio(self, response: scrapy.http.Response, author: Dict[str, str]):
        bio_div = response.css("div.postbody *::text").extract()
        bio, is_valid_bio = "", True
        for text in bio_div:
            if "la biographie de cet auteur est vide." in clean_html_text(text).lower():
                is_valid_bio = False

        if is_valid_bio:
            bio = " ".join([text for text in bio_div if clean_html_text(text)])

        author["biography"] = bio

        yield AuthorsItem(**author)
