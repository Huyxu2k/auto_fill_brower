from selenium.webdriver.common.by import By
from pages.base import BaseForm

class TestPage(BaseForm):
    SEARCH_INPUT = (By.CSS_SELECTOR, '#search')
    