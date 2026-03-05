from selenium.webdriver.common.by import By
from pages.base import BaseForm
from models.person import Person

class TestPage(BaseForm):
    URL = "https://dichvucong.gov.vn/p/home/dvc-tra-cuu-ho-so.html"
    # textbox
    MA_HO_SO = (By.ID, 'maHSB')
    MA_BAO_MAT = (By.ID, 'ipCaptchaB')
    
    # button
    TRA_CUU = (By.ID, 'btnSubmitB')

    def __init__(self, browser, timeout = 10 , url = URL):
        self.url = url
        super().__init__(browser)
    
    def open(self):
        self.browser.get(self.url)

    def fill(self, person: Person):
        input_ma_hs = self.get(self.MA_HO_SO)
        input_ma_hs.clear()
        input_ma_hs.send_keys(person.name)

        input_captcha = self.get(self.MA_BAO_MAT)
        input_captcha.clear()
        input_captcha.send_keys(person.yob)

        self.wait()

    def click_btn(self):
        self.click(self.TRA_CUU)