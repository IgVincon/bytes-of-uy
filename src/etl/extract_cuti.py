"""This is the extract_cuti module.

This module performs the extraction phase (of an ETL pipeline) for a
website by scraping data of IT events. It uses the scraper module.
"""

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from json import dump

from utils.scraper import extract_links, fetch_url, find_element, scrape

def extract():
    URL = 'https://cuti.org.uy/eventos/'
    LINKS_CSS_SELECTORS = [
        '#mec_full_calendar_container_1779',
        '.mec-export-details',
    ]
    CSS_SELECTOR_LIST = [
        '.mec-single-title',
        '#mec_local_time_details',
        '.mec-single-event-location',
        '.mec-single-event-description',
    ]
    DATA_SET_FORMAT = {
        'title': [],
        'date_time': [],
        'place': [],
        'description': [],
        'add_to_calendar': [],
        'url': [],
        'uuid4': [],
    }
    response = fetch_url(URL) # considerar caso en que la request no de 200 OK y que necesite manejar esa situación. Considerar retry en caso de timeout
    element = find_element(response, LINKS_CSS_SELECTORS[0])
    urls = extract_links(element) # considerar caso en que no haya eventos ese mes (o hasta el momento de ese mes) y como manejar esa situación
    data_set = scrape(urls, CSS_SELECTOR_LIST,
                      LINKS_CSS_SELECTORS[1], DATA_SET_FORMAT)
    with open('data/raw/cuti_extraction.json', 'w') as file:
        dump(data_set, file)