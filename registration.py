
from datetime import datetime as dt
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from settings import botva_pass, botva_login, name_id


def registration(namelist, email, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('window-size=1200x600')
    brow = webdriver.Chrome(chrome_options=options)
    brow.implicitly_wait(2)
    brow.get('http://avatar.botva.ru/')

    element = WebDriverWait(brow, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'sign_in'))
                        )

    for name in namelist:
        namefield = brow.find_element_by_css_selector("input.required")
        namefield.send_keys(name)

        try:
            namefield.parent.find_element_by_class_name('iright')
            break

        except:  # need next name
            namefield.clear()

    brow.find_element_by_class_name("play_button").click()

    for _ in range(2):
        time.sleep(2)
        if "index.php" in brow.current_url:
            break

    btns = brow.find_elements_by_class_name("button_new")
    for btn in btns:
        if btn.text == "ПЕРЕЙТИ":
            btn.click()
            break

    brow.find_element_by_id('guild_link').click()

    element = WebDriverWait(brow, 10).until(
                            EC.presence_of_element_located((By.NAME, 'email'))
                        )

    brow.find_element_by_name('email').send_keys(email)

    brow.find_element_by_name('accept').click()

    brow.find_element_by_name('password').send_keys(pswrd)
    brow.find_element_by_name('password2').send_keys(pswrd + Keys.ENTER)


if __name__ == "__main__":


    email = botva_login.replace(str(name_id), str(name_id+1))
    names = ["MrSmith-%s" % str(name_id+1),
            ]


    with open("settings.py", 'r') as f:
        st = f.read()
        start_login = st.find('\nbotva_login')
        end_login = st.find('\n', start_login+1)

        actual_login = st[start_login:end_login]

        st = st[:start_login+1] + "# " + st[start_login+1:end_login] + "\n" + "botva_login = " + "'" + email + "'" + st[end_login:]
        st = st.replace("name_id = " + str(name_id), "name_id = " + str(name_id+1))


    registration(names, email, botva_pass)


    with open("settings.py", 'w') as f:
        f.write(st)

