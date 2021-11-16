from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
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
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome()
        # self.driver.set_window_size(1024, 780)

    def login(self, login, password):
        self.driver.get('https://web.skype.com/')

        # try to find login field by id or name
        for _ in range(10):  # check for 20 seconds (10 times by 2 sec)
            try:
                login_field = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.ID, 'username'))  # id='i0116'
                )
                break
            except TimeoutException:
                pass
            try:
                login_field = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.NAME, 'loginfmt'))
                )
                break
            except TimeoutException:
                pass

        login_field.send_keys(login + Keys.ENTER)  # write login

        time.sleep(1.5)  # wait site script start work correctly
        # search pass field
        pass_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'i0118'))
        )
        pass_field.send_keys(password + Keys.ENTER)  # entering pswrd

        # working with alerts
        try:
            time.sleep(0.5)
            self.driver.find_element(By.ID, 'KmsiCheckboxField').click()
            time.sleep(0.2)
            self.driver.find_element(By.ID, 'idBtn_Back').click()
        except:
            pass
        
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'button')]")))
        time.sleep(4)
        btns = self.driver.find_elements(By.XPATH, "//div[contains(@role, 'button')]")
        for btn in btns:
            try:
                btn.click()
                break
            except:
                continue
        time.sleep(1)

    def select_chat(self, chatname):
        try:
            chat = self.driver.find_element(By.XPATH, f"//div[contains(@aria-label, '{chatname}')]")
            chat.click()
        except WebDriverException:
            self.driver.save_screenshot("screenWebDriverException.png")

    def send_message(self, message):
        while True:
            try:
                text_area = self.driver.find_element(By.CLASS_NAME, "public-DraftEditor-content")
                text_area.send_keys(message + Keys.ENTER)
                break
            except:
                pass


if __name__ == '__main__':

    from settings import skype_login, skype_pass, skype_groups, skype_admin

    skypesender = SkypeSender()
    skypesender.login(skype_login, skype_pass)
    # chat_grops = skype_groups

    skypesender.select_chat(skype_admin)
    skypesender.send_message(f'start {time.time()}')

    time.sleep(1)
    skypesender.driver.quit()

