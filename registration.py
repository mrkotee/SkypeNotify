import sys
import os
import time
from random import randint
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def registration(namelist, email, password, test=False):
    """register ONE new bot from gived namelist
        return False if all of gived names alredy registered
        or if gived email alredy registered"""

    if test:
        screen_dir_path = os.path.join(os.getcwd(), 'screen')
        if not os.path.exists(screen_dir_path):
            os.mkdir(screen_dir_path)

    def screen_for_test(filename, _webdriver):  # if test == True save screen in working dir
        if test:
            print(filename)
            filepath = os.path.join(screen_dir_path, f'{filename}.png')
            with open(filepath, 'wb') as f:
                f.write(_webdriver.get_screenshot_as_png())

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument('window-size=1200x600')
    brow = webdriver.Chrome(options=options)
    brow.implicitly_wait(2)

    try:
        for i, name in enumerate(namelist):
            if len(name) > 19:
                continue
            if name == namelist[i - 1]:
                brow.close()
                time.sleep(20)
                brow = webdriver.Chrome(chrome_options=options)
                brow.implicitly_wait(2)

            brow.get('http://avatar.botva.ru/')
            WebDriverWait(brow, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sign_in'))
            )

            namefield = brow.find_element(By.CSS_SELECTOR, "input.required")
            namefield.send_keys(name + Keys.ENTER)

            time.sleep(1)

            screen_for_test('login start', brow)

            try:
                namefield.parent.find_element(By.CLASS_NAME, 'iright')

            except:  # try login with given name
                time.sleep(2)
                namefield.parent.find_element(By.CLASS_NAME, 'iwrong')
                namefield.clear()
                brow.find_element(By.CLASS_NAME, 'sign_in').click()
                time.sleep(0.5)
                brow.find_element(By.CLASS_NAME, 'form_trigger_name').click()
                time.sleep(0.3)
                namefield = brow.find_element(By.CSS_SELECTOR, '.form5 > div:nth-child(1) > input:nth-child(1)')
                namefield.send_keys(name)

            brow.find_element(By.CLASS_NAME, "play_button").click()
            try:
                time.sleep(0.4)
                brow.find_element(By.CLASS_NAME, "play_button").click()
            except:
                pass

            screen_for_test('login end', brow)

            try:
                WebDriverWait(brow, 10).until(
                    EC.presence_of_element_located((By.ID, 'm1'))
                )
                time.sleep(2)
                brow.find_element(By.ID, 'm1').click()
                if "index.php" in brow.current_url:
                    break
            except:
                if i == len(namelist):
                    return False
                continue

        screen_for_test('login success', brow)

        btns = brow.find_elements(By.CLASS_NAME, "button_new")
        for btn in btns:
            if btn.text == "ПЕРЕЙТИ":
                btn.click()
                break

        guild_link = WebDriverWait(brow, 10).until(
            EC.presence_of_element_located((By.ID, 'guild_link'))
        )
        try:
            guild_link.click()
        except WebDriverException:
            time.sleep(0.7)
            brow.find_element(By.ID, 'guild_link').click()

        screen_for_test('guide link finded', brow)

        email_field = WebDriverWait(brow, 10).until(
            EC.presence_of_element_located((By.NAME, 'email'))
        )

        email_field.send_keys(email)

        brow.find_element(By.NAME, 'accept').click()

        brow.find_element(By.NAME, 'password').send_keys(password)
        brow.find_element(By.NAME, 'password2').send_keys(password + Keys.ENTER)

        screen_for_test('registration end', brow)

        try:
            time.sleep(1)
            brow.find_element(By.NAME, 'email')
            brow.close()
            return False, 'Possibly wrong/already used email'
        except:
            brow.close()
            return True

    except Exception as e:
        # brow.close()
        print(e)
        print('registration unsuccessful ')
        brow.close()


if __name__ == "__main__":

    from settings import botva_pass, botva_login, name_id

    test = False

    if 'test' in sys.argv:
        test = True
        num = randint(12, 3000)
        email = botva_login.replace(str(name_id), str(num))
        email = 'one' + str(randint(1, 32)) + email
        names = [f"TheOne-{num}",
                 f"TheOne-{num}",
                 ]

    elif 'new' in sys.argv:
        email = botva_login.replace(str(name_id), str(name_id + 1))
        names = [f"MrSmith-{name_id + 1}",
                 ]
    else:
        print('not enough args')

    if 'new' in sys.argv:
        with open("settings.py", 'r') as f:
            st = f.read()
            start_login = st.find('\nbotva_login')
            end_login = st.find('\n', start_login + 1)

            actual_login = st[start_login:end_login]

            st = st[
                 :start_login + 1] + "# " + st[
                            start_login + 1:end_login] + "\n" + "botva_login = " + "'" + email + "'" + st[
                                                                                                    end_login:]
            st = st.replace("name_id = " + str(name_id), "name_id = " + str(name_id + 1))

    if 'new' in sys.argv or 'test' in sys.argv:
        print(names, email, botva_pass)
        print()
        registration(names, email, botva_pass, test)

    if 'new' in sys.argv:
        with open("settings.py", 'w') as f:
            f.write(st)
