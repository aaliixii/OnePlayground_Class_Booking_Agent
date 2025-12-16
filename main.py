from playwright.sync_api import sync_playwright
import logging
import datetime
from filters import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL_1 = 'https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/cd5263ebda/schedule'
URL_2 = 'https://clients.mindbodyonline.com/classic/mainclass'

if __name__ == '__main__':
    selection = ['Jaclyn Bogdanovic', '05:00PM', 'Newtown One Playground']
    date = "2025-12-17"
    
    with sync_playwright() as spw:
        browser, page = page_init(spw, URL_1)
        data = evaluate_page(page)
        # print(data)
        select_date(page, date)
        update_filters(page, [selection[-1]], class_types=['Reformer', 'Yoga Series'])
        screenshot(page, ele = 'Final')