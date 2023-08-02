from requests import Response
from requests_html import HTMLSession, user_agent, Element
from typing import Any
from uuid import uuid4
from time import sleep

def fetch_url(url: str) -> Response:
    headers = {'user-agent': user_agent()}
    session = HTMLSession()
    response = session.get(url, headers = headers, timeout = 10)
    response.raise_for_status()
    sleep(5)
    return response

def find_element(
        response: Response, css_selector: str,
        first_only: bool = True) -> Element|str:
    # Si first_only = False devuelve una list[Element]? Tener en cuenta
    element = response.html.find(css_selector, first = first_only)
    element = 'n/a' if element is None else element
    return element

def extract_urls(element: Element) -> list[str]:
    # Caso limite: absolute_links no encuentra url. Regresa None? Pensar como manejarlo
    urls = element.absolute_links
    return list(urls)

def extract_data(
        response: Response, css_selectors: list[str]) -> list[str | list[str]]:
    # Es posible poner con type hints tipo de dato extract_urls? Es decir, es un tipo de dato del resultado de esa función
    element_list = [
        find_element(response, selector) for selector in css_selectors[:-1]
    ]
    data = [ele.text if ele != 'n/a' else ele for ele in element_list]
    links = find_element(response, css_selectors[-1])
    links = extract_urls(links) if links != 'n/a' else links
    data.append(links)
    return data

def store_data(
        data_set_format: dict[str: list], data: list[str | list[str]],
        url: str) -> dict[ str: list[str | list[str]] ]:
    local_copy = data_set_format
    uuid = str(uuid4())
    data.append(url)
    data.append(uuid)
    for key, value in zip(local_copy.keys(), data):
        local_copy[key].append(value)
    return local_copy

def scrape(
        urls: list[str], css_selectors: list[str],
        data_set_format: dict[str: list]) -> dict[ str: list[str | list[str]] ]:
    for url in urls:
        response = fetch_url(url)
        data = extract_data(response, css_selectors)
        data_set = store_data(data_set_format, data, url)
    return data_set