from utils.web_scraper import fetch_url, find_elements, extract_urls, scrape
from requests.exceptions import ConnectionError, InvalidSchema, ReadTimeout
from pyppeteer.errors import TimeoutError

def main():
    url = 'https://cuti.org.uy/eventos/'
    css_selector = '#mec_full_calendar_container_1779'

    try:
        response = fetch_url(url)
        element = find_elements(response, css_selector)
        urls = extract_urls(element)
        data_set = scrape(urls)
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

if __name__ == "__main__":
    main()