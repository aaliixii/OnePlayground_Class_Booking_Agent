from playwright.sync_api import Page, Browser, sync_playwright, Playwright
import time
URL_1 = 'https://brandedweb-next.mindbodyonline.com/components/widgets/schedules/view/cd5263ebda/schedule'
URL_2 = 'https://clients.mindbodyonline.com/classic/mainclass'

def run(playwright: Playwright):
    browser = playwright.firefox.launch()
    page = browser.new_page()
    page.goto(URL_1)
    browser.close()

def screenshot(playwright: Playwright, url) -> None:
    browser = playwright.firefox.launch()
    page = browser.new_page()
    
    page.goto(URL_1)
    time.sleep(5)
    
    page.screenshot(path = 'test_screenshot.png', full_page = True)
    print(evaluate_page(page))
    browser.close()

def evaluate_page(page: Page):
    with open('eval.js', '+r') as f:
        return page.evaluate(f.read())

if __name__ == '__main__':
    with sync_playwright() as spw:
        screenshot(spw, URL_1)