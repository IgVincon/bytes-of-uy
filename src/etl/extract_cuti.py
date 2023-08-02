from utils.web_scraper import fetch_url, find_element, extract_urls, scrape
from requests.exceptions import ConnectionError, InvalidSchema, ReadTimeout
from pyppeteer.errors import TimeoutError
from json import dump, dumps

def extract():
    url = 'https://cuti.org.uy/eventos/'
    css_selector = '#mec_full_calendar_container_1779'
    css_selector_list = [
        '.mec-single-title',
        '#mec_local_time_details',
        '.mec-single-event-location',
        '.mec-single-event-description',
        '.mec-export-details',
    ]
    data_set_format = {
        'title': [],
        'date_time': [],
        'place': [],
        'description': [],
        'add_to_calendar': [],
        'url': [],
        'uuid4': [],
    }

    try:
        response = fetch_url(url) # considerar caso en que la request no de 200 OK y que necesite manejar esa situación. Considerar retry en caso de timeout
        element = find_element(response, css_selector)
        urls = extract_urls(element) # considerar caso en que no haya eventos ese mes (o hasta el momento de ese mes) y como manejar esa situación
        data_set = scrape(urls, css_selector_list, data_set_format)
        #with open('data/raw/cuti_extraction.json', 'w') as file:
        #    dump(data_set, file)
        print(data_set)
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