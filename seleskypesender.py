from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SkypeSender():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

		# options.add_argument('window-size=1200x600')
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(chrome_options=options)
        # self.driver = webdriver.Chrome()
        # self.driver.set_window_size(1024, 780)

    def login(self, login, password):
        self.driver.get('https://web.skype.com/')
        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'username')))
        time.sleep(5)
        while True:
            try:
                self.driver.find_element_by_id('username').send_keys(login + Keys.ENTER)
                break
            except:
                self.driver.find_element_by_name('loginfmt').send_keys(login + Keys.ENTER)
                break

        time.sleep(4)
        
        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'i0118')))
        # try:
        self.driver.find_element_by_id('i0118').send_keys(password + Keys.ENTER)
        # except:
        #     self.driver.find_element_by_name('passwd').send_keys(password + Keys.ENTER)
        # self.driver.find_element_by_id('idSIButton9').click()
        # time.sleep(10)
        
        time.sleep(0.5)
        try:
            self.driver.find_element_by_id('KmsiCheckboxField').click()
            time.sleep(0.2)
            self.driver.find_element_by_id('idBtn_Back').click()
        except:
            pass
        
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'button')]")))
        time.sleep(4)
        btns = self.driver.find_elements_by_xpath("//div[contains(@role, 'button')]")
        for btn in btns:
            try:
                btn.click()
                break
            except:
                continue
        time.sleep(1)


    def select_chat(self, chatname):
        # chats = self.driver.find_elements_by_css_selector(
        #             'span > h4 > span.topic')
        # for chat in chats:
        #     if chat.text == chatname:
        #         while True:
        #             try:
        #                 chat.click()
        #                 break
        #             except:
        #                 pass
        #         break

        chat = self.driver.find_element_by_xpath("//div[contains(@aria-label, '{chatname}')]".format(chatname=chatname))
        chat.click()


    def send_message(self, message):
        while True:
            try:
                # text_area = self.driver.find_element_by_id('chatInputAreaWithQuotes')
                text_area = self.driver.find_element_by_class_name("public-DraftEditor-content")
                text_area.send_keys(message + Keys.ENTER)
                break
            except:
                pass


if __name__ == '__main__':
    
    skype_login, skype_pass = 'mrkotee08@ya.ru', "mcvUjB9b"

    skypesender = SkypeSender()
    skypesender.login(skype_login, skype_pass)
    # chat_grops = skype_groups

    skype_admin = 'MrKotee ev'
    skypesender.select_chat(skype_admin)
    skypesender.send_message('start')

