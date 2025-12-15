from playwright.sync_api import sync_playwright
import logging
from filters import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_1 = 'https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/cd5263ebda/schedule'
URL_2 = 'https://clients.mindbodyonline.com/classic/mainclass'

if __name__ == '__main__':
    selection = ['Jaclyn Bogdanovic', '05:00PM', 'Newtown One Playground']
    with sync_playwright() as spw:
        browser, page = page_init(spw, URL_1)
        data = evaluate_page(page)
        print(data)
        update_filters(page, [selection[-1]], class_types=['Reformer', 'Mat Pilates'])
        screenshot(page, ele = 'Final')