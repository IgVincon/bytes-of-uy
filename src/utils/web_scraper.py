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

def find_elements(
    response: Response, css_selector: str, first_only: bool = True
) -> Element|list[Element]|None:
    elements = response.html.find(css_selector, first = first_only)
    return elements

def extract_urls(elements: Element) -> list[str]: #absolute_links regresa None si no encuentra urls? Que hago en ese caso? Habria que crear un handle para eso
    urls = elements.absolute_links
    return list(urls)

def extract_data(response: Response) -> list[str|list[str]]: #revisar como poner que en vez de set[str] en realidad es tipo de dato extract_urls
    uuid = str(uuid4())
    title = find_elements(response, '.mec-single-title').text
    date_time = find_elements(response, '#mec_local_time_details').text
    place = (
        'n/a' if find_elements(response, '.mec-single-event-location') is None
        else find_elements(response, '.mec-single-event-location').text
    )
    description = find_elements(response, '.mec-single-event-description').text
    add_to_calendar = (
        'n/a' if find_elements(response, '.mec-export-details') is None
        else extract_urls( find_elements(response, '.mec-export-details') )
    )
    data = [uuid, title, date_time, place, description, add_to_calendar]
    return data

def scrape(urls: list[str]) -> dict[str: list[str|list[str]]]:
    results = {
        'uuid4': [],
        'title': [],
        'date_time': [],
        'place': [],
        'description': [],
        'add_to_calendar': [],
        'url': [],
    }
    for url in urls:
        response = fetch_url(url)
        data = extract_data(response)
        data.append(url)
        for key, value in zip(results.keys(), data):
            results[key].append(value)
    return results