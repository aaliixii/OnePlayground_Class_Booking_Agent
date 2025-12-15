from playwright.sync_api import Page, Browser, sync_playwright, Playwright
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATE = 0

def page_init(playwright:Playwright, url:str) -> tuple[Browser, Page]:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(url)
    return browser, page

def screenshot(page, ele = None) -> None:
    time.sleep(0.5)
    if ele:
        logger.info(f'Screenshotting view!')
        page.screenshot(path = f'output/{ele}_screenshot.png')
        return
    logger.info(f'Screenshotting page!')
    page.screenshot(path=f'output/{STATE}_view_screenshot.png', fullPage=True)

def evaluate_page(page:Page) -> list:
    with open('filters_finder.js', '+r') as f:
        page_data = list(page.evaluate(f.read()))
    return page_data

def click(page:Page, text:str) -> None:
    try:
        target = page.get_by_text(text, exact=False).first
        target.wait_for(state='visible', timeout=5000)
    
        logger.info(f"Clicking: {text}")
        target.click()
        page.wait_for_load_state("domcontentloaded")
    except TimeoutError:
        logger.warning(f"Element {text} never appeared.")

def backdrop_check(page:Page):
    backdrop = 'div.MuiBackdrop-root'
    try:
        backdrop = page.locator(backdrop).first
        if backdrop.is_visible(timeout=200):
            logger.warning(f'View Obstruction: Resetting state')
            page.keyboard.press('Escape')
            backdrop.wait_for(state='hidden', timeout=3000)
            logger.info(f'View Reset')
    except TimeoutError:
        pass
    except Exception as e:
        logger.error(f'Failed to reset view: {e}')
        sys.exit()


def scroll_and_click(page: Page, text: str):
    logger.info(f"Looking for option: '{text}'...")
    menu = page.locator("div[role='presentation']")
    
    if not menu.is_visible():
        logger.error("Menu not open! Cannot scroll.")
        return
    menu.click(position={"x": 10, "y": 10})
    
    max_retries = 50
    for _ in range(max_retries):
        target = menu.get_by_text(text, exact=False).first
        if target.is_visible():
            logger.info(f"Found '{text}'. Clicking.")
            target.click()
            return

        prev_scroll = menu.evaluate("(el) => el.scrollTop")
        page.keyboard.press("ArrowDown")
        time.sleep(0.1)
        new_scroll = menu.evaluate("(el) => el.scrollTop")
        
        if prev_scroll == new_scroll:
            page.keyboard.press("ArrowDown")
            if menu.evaluate("(el) => el.scrollTop") == prev_scroll:
                logger.warning(f"Reached end of list. '{text}' not found.")
                break
    logger.error(f"Failed to find '{text}'")

def update_filters(page: Page, locations:list[str] = [], 
                    class_types:list[str] = []):
    logger.info(f'update_filters | locations: {locations}, class_types: {class_types}')
    if locations:
        click(page, 'Location')
        
        for loc in locations:
            logger.info(f'Selecting Location: {loc}')
            scroll_and_click(page, loc)
        backdrop_check(page)
    
    if class_types:
        click(page, 'Class Type')
        for loc in class_types:
            logger.info(f'Selecting Class Type: {loc}')
            scroll_and_click(page, loc)
        backdrop_check(page)
    logger.info(f'Filters Applied.')


