
import sys, os
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


def registration(namelist, email, password, test=False):
    """register ONE new bot from gived namelist
        return False if all of gived names alredy registered
        or if gived email alredy registered"""

    def screen_for_test(filename, _webdriver):
        if test:
            filepath = os.path.join(os.getcwd(), 'screen', '%s.png' % filename)
            with open(filepath, 'wb') as f:
                f.write(_webdriver.get_screenshot_as_png())

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument('window-size=1200x600')
    brow = webdriver.Chrome(chrome_options=options)
    brow.implicitly_wait(2)

    try:
        for i, name in enumerate(namelist):
            if name == namelist[i-1]:
                brow.close()
                time.sleep(20)
                brow = webdriver.Chrome(chrome_options=options)
                brow.implicitly_wait(2)

            brow.get('http://avatar.botva.ru/')
            element = WebDriverWait(brow, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'sign_in'))
                            )

            print("try to login")

            namefield = brow.find_element_by_css_selector("input.required")
            namefield.send_keys(name + Keys.ENTER)

            time.sleep(1)

            screen_for_test('login start', brow)


            try:
                namefield.parent.find_element_by_class_name('iright')

            except:  # try login with gived name
                time.sleep(2)
                namefield.parent.find_element_by_class_name('iwrong')
                namefield.clear()
                brow.find_element_by_class_name('sign_in').click()
                time.sleep(0.5)
                brow.find_element_by_class_name('form_trigger_name').click()
                time.sleep(0.3)
                namefield = brow.find_element_by_css_selector('.form5 > div:nth-child(1) > input:nth-child(1)')
                namefield.send_keys(name)

            brow.find_element_by_class_name("play_button").click()
            try:
                time.sleep(0.4)
                brow.find_element_by_class_name("play_button").click()
            except:
                pass

            screen_for_test('login end', brow)

            try:            
                element = WebDriverWait(brow, 10).until(
                                EC.presence_of_element_located((By.ID, 'm1'))
                            )
                # for _ in range(2):
                time.sleep(2)
                brow.find_element_by_id('m1').click()
                if "index.php" in brow.current_url:
                    break
            except:
                if i == len(namelist):
                    return False
                continue

        print("login successful")
        screen_for_test('login success', brow)

        btns = brow.find_elements_by_class_name("button_new")
        for btn in btns:
            if btn.text == "ПЕРЕЙТИ":
                btn.click()
                break

        print("first quest btn clicked")

        element = WebDriverWait(brow, 10).until(
                            EC.presence_of_element_located((By.ID, 'guild_link'))
                        )
        try:
            brow.find_element_by_id('guild_link').click()
        except WebDriverException:
            # if "black_overlay" in e:
            time.sleep(0.7)
            brow.find_element_by_id('guild_link').click()

        screen_for_test('guide link finded', brow)

        print("guide link finded")

        # try:
        #     element = WebDriverWait(brow, 15).until(
        #                         EC.presence_of_element_located((By.CLASS_NAME, 'popup_my_container'))
        #                     )
        # except Exception as e:
        #     with open('page.html', 'w') as f:
        #         f.write(str(brow.page_source))

        element = WebDriverWait(brow, 10).until(
                                EC.presence_of_element_located((By.NAME, 'email'))
                            )

        print('entering email')
        brow.find_element_by_name('email').send_keys(email)

        brow.find_element_by_name('accept').click()

        print('entering password')
        brow.find_element_by_name('password').send_keys(password)
        brow.find_element_by_name('password2').send_keys(password + Keys.ENTER)

        screen_for_test('registration end', brow)

        try:
            time.sleep(1)
            brow.find_element_by_name('email')
            return False
        except:
            return True

    except Exception as e:
        # brow.close()
        print(e)
        
    else:
        brow.close()


if __name__ == "__main__":
    # names = ['TheOne-1893', 'TheOne-465', 'TheOne-2319', 'TheOne-214', 'TheOne-1950']
    # names = ['ssdtheone123', 'mrsssmith', 'theone123']
    # email = 'adflkjsdsldkfjaa@gmail.com'
    # pswrd = 'Qwerty78'

    # print(registration(names, email, pswrd, test=True))


    if 'test' in sys.argv:
        test = True
        num = randint(12, 3000)
        email = botva_login.replace(str(name_id), str(num))
        email = 'one' + str(randint(1, 32)) + email
        names = ["TheOne-%s" % str(num),
                "TheOne-%s" % str(num),
                ]

    elif 'new' in sys.argv:
        test = False
        email = botva_login.replace(str(name_id), str(name_id+1))
        names = ["MrSmith-%s" % str(name_id+1),
                ]
    else:
        print('not enough args')

    if 'new' in sys.argv:
        with open("settings.py", 'r') as f:
            st = f.read()
            start_login = st.find('\nbotva_login')
            end_login = st.find('\n', start_login+1)

            actual_login = st[start_login:end_login]

            st = st[:start_login+1] + "# " + st[start_login+1:end_login] + "\n" + "botva_login = " + "'" + email + "'" + st[end_login:]
            st = st.replace("name_id = " + str(name_id), "name_id = " + str(name_id+1))

    if 'new' in sys.argv or 'test' in sys.argv:
        print(names, email, botva_pass)
        print()
        registration(names, email, botva_pass, test)

    if 'new' in sys.argv:
        with open("settings.py", 'w') as f:
            f.write(st)

    # print('fail')
