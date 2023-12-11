import re
import urllib.parse
from typing import Dict, List, Union

import requests
from bs4 import BeautifulSoup, Tag

COMICS_QUERY = "https://www.bdphile.fr/search/album/?q={}"


def _clean_html_text(text: str):
    text = text.replace("\n", " ").replace("\t", " ").strip()
    text = re.sub(
        r" +",
        " ",
        text,
    )
    return text


def get_href(tag: Tag):
    a_tag = tag.find("a")
    return a_tag.attrs["href"] if a_tag else ""


def search(query: str) -> List[Dict[str, str]]:
    """
    Send a request to www.bdphile.fr to get a relevant list of comics matching the query.
    """
    response = requests.get(COMICS_QUERY.format(query))
    soup = BeautifulSoup(response.text, features="lxml")

    results = soup.find("div", attrs={"class": "col-lg-7"})

    parsed_links = []
    for tag in results:
        if tag.name:
            if tag.name == "br":
                parsed_links[-1]["year"] = tag.previous_element.replace("-", "").strip()
            elif tag.name == "a":
                parsed_links.append({"text": tag.text, "url": tag["href"]})

    return parsed_links[:-1]


def getComicData(url: str) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Get the metadata of a comics from a trageted url
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")

    section = soup.find("section", attrs={"class": "details-section"})

    data = {}

    data["Série"] = {"text": _clean_html_text(section.find("h1").get_text()), "url": ""}
    data["Titre"] = {"text": _clean_html_text(section.find("h2").get_text()), "url": ""}

    dl = section.find("dl")
    keys = dl.find_all("dt")
    values = dl.find_all("dd")

    data.update(
        {
            _clean_html_text(key.text): {
                "text": _clean_html_text(value.text),
                "url": get_href(value),
            }
            for key, value in zip(keys, values)
        }
    )
    data["img"] = section.find("img")["src"]

    return data


def getAuthorData(author_url: str) -> Dict[str, str]:
    """
    Get the metadata of a targeted url's author
    """

    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, features="lxml")

    name = soup.find("h1").get_text()
    nick_name = ""
    if "(" in name and ")" in name:
        start = name.index("(")
        end = name.index(")")

        nick_name = name[:start]
        full_name = name[start + 1 : end]

    else:
        full_name = name

    first_name, *last_name = full_name.split(" ")
    last_name = " ".join(last_name)

    activity = soup.find("h2").get_text()

    author_bio_url = author_url.replace("view", "bio")
    response = requests.get(author_bio_url)
    soup = BeautifulSoup(response.text, features="lxml")
    bio_div = soup.find("div", {"class": "postbody"})
    bio = bio_div.get_text()

    return {
        "first_name": first_name,
        "last_name": last_name,
        "nick_name": nick_name,
        "activity": activity,
        "biography": bio,
    }


if __name__ == "__main__":
    getComicData("https://www.bdphile.fr/album/view/6665/")
