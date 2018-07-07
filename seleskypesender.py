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
        self.driver.get('https://web.skype.com/ru/')
        # WebDriverWait(self.driver, 20).until(
        #     EC.presence_of_element_located((By.ID, 'username')))
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
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'topic')))

    def select_chat(self, chatname):
        chats = self.driver.find_elements_by_css_selector(
                    'span > h4 > span.topic')
        for chat in chats:
            if chat.text == chatname:
                while True:
                    try:
                        chat.click()
                        break
                    except:
                        pass
                break

    def send_message(self, message):
        while True:
            try:
                text_area = self.driver.find_element_by_id('chatInputAreaWithQuotes')
                text_area.send_keys(message + Keys.ENTER)
                break
            except:
                pass
