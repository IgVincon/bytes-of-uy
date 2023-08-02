"""This module contains functions for scraping websites."""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from time import sleep
from typing import Any
from uuid import uuid4

from pyppeteer.errors import TimeoutError
from requests import Response
from requests.exceptions import ConnectionError, InvalidSchema, ReadTimeout
from requests_html import Element, HTMLSession, user_agent

def fetch_url(url: str) -> Response:
    headers = {'user-agent': user_agent()}
    session = HTMLSession() # Necesito una sesión para cada URL?
    try:
        response = session.get(url, headers = headers, timeout = 30)
        response.raise_for_status()
        sleep(5)
        return response
    except InvalidSchema as e:
        # error for 'h**ps://www.google.com/'
        print(f'For the url "{url}" the error is: {e} \n')
        pass
    except ReadTimeout as e:
        # error due to too much delay
        print(f'For the url "{url}" the error is: {e} \n')
        pass
    except ConnectionError as e:
        # error for 'https://www.baaaadurl.com/'
        print(f'For the url "{url}" the error is: {e} \n')
        pass
    except TimeoutError as e:
        # error if timout in rendering the page
        print(f'For the url "{url}" the error is: {e} \n')
        pass

def find_element(
        response: Response, css_selector: str,
        first_only: bool = True) -> Element|str:
    # Si first_only = False devuelve una list[Element]? Tener en cuenta
    element = response.html.find(css_selector, first = first_only)
    element = 'n/a' if element is None else element
    return element

def extract_links(element: Element) -> list[str]:
    # Caso limite: absolute_links no encuentra url. Regresa None? Pensar como manejarlo
    return list(element.absolute_links)

def combine_data(
        ele_list: list[Element], links_ele: Element,
        url: str) -> list[str | list[str]]:
    links = extract_links(links_ele) if links_ele != 'n/a' else links_ele
    data = [ele.text if ele != 'n/a' else ele for ele in ele_list]
    data.append(links)
    data.append(url)
    data.append( str(uuid4()) )
    return data

def store_data(
        data_set_format: dict[str: list],
        data: list[str | list[str]]) -> dict[ str: list[str | list[str]] ]:
    local_copy = data_set_format
    for key, value in zip(local_copy.keys(), data):
        local_copy[key].append(value)
    return local_copy

def scrape(
        urls: list[str], css_selectors: list[str], link_css_selector: str,
        data_set_format: dict[str: list]) -> dict[ str: list[str | list[str]] ]:
    for url in urls:
        response = fetch_url(url)
        element_list = [
            find_element(response, selector) for selector in css_selectors
        ]
        links_element = find_element(response, link_css_selector)
        data = combine_data(element_list, links_element, url)
        data_set = store_data(data_set_format, data) #how does this even work?
    return data_set