from requests import Response
from requests_html import HTMLSession, user_agent, Element
from typing import Any
from uuid import uuid4
import time

def fetch_url(url: str) -> Response:
    headers = {'user-agent': user_agent()}
    session = HTMLSession()
    response = session.get(url, headers = headers, timeout = 10)
    response.raise_for_status()
    time.sleep(5)
    return response

def find_elements(
    response: Response, css_selector: str, first_only: bool = True
) -> Element|list[Element]|None:
    elements = response.html.find(css_selector, first = first_only)
    return elements

def extract_urls(elements: Element) -> set[str]:
    urls = elements.absolute_links
    return urls

def extract_data(response: Response, url: str) -> dict[str, str|set[str]]: #revisar como poner que en vez de set[str] en realidad es tipo de dato extract_urls
    title = find_elements(response, '.mec-single-title')
    date_time = find_elements(response, '#mec_local_time_details')
    place = (
        'n/a' if find_elements(response, '.mec-single-event-location') is None
        else find_elements(response, '.mec-single-event-location').text
    )
    description = find_elements(response, '.mec-single-event-description')
    add_to_calendar = (
        'n/a' if find_elements(response, '.mec-export-details') is None
        else find_elements(response, '.mec-export-details')
    )
    data = {
        'uuid4': uuid4(), #revisar formato
        'title': title.text,
        'date_time': date_time.text,
        'place': place,
        'description': description.text,
        'add_to_calendar': (
            add_to_calendar if add_to_calendar == 'n/a'
            else extract_urls(add_to_calendar)
        ),
        'url': url,
    }
    return data

def scrape(urls) -> list[dict]:
    results = []
    for url in urls:
        response = fetch_url(url)
        data = extract_data(response, url)
        results.append(data)
    return results