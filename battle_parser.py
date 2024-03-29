import re, time
from robobrowser import RoboBrowser
from datetime import datetime as dt
from datetime import timedelta
from settings import botva_pass, botva_login, btl_filepath, bot_dir_path
from requests.exceptions import ConnectionError
import json
import logging


class TimerParser():
    USERAGENT = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    part_resurs = ['Сено', 'Ягоды', 'ЗБ', 'Самоцветы', 'Самоцветы', 'Ягоды', 'Сено', 'Вода', 'Вода',
                   'Железо', 'Железо', 'Соль', 'Ягоды', 'Адамант', 'Железо', 'ЗС', 'Ягоды', 'Соль']
    part_names = [
        'Золотое предгорье',
        'Верхнее Шелкопрядье',
        'Земли Барантусов',
        'Самоцветная гряда',
        'Самоцветное ущелье',
        'Ягодная опушка',
        'Золотой берег',
        'Пресноводье',
        'Бродолесье',
        'Перевал Дятлов',
        'Подножье',
        'Соляные пещеры',
        'Нижнее шелкопрядье',
        'Вершина мира',
        'Центральный пляж',
        'Земли Свинтусов',
        'Ягодная поляна',
        'Соляные залежи'
    ]

    def __init__(self):
        self.btl_timers = {}
        self.update_timer = False

    def read_btl_file(self):
        json_load = json.load(open(btl_filepath, 'r'))
        self.btl_timers = json_load['timers']
        self.update_timer = json_load['update_timer']

    def write_btl_to_file(self):
        json.dump(
            {'timers': self.btl_timers, 'update_timer': self.update_timer}, 
            open(btl_filepath, 'w')
            )

    def parse_timers(self):
        """Parse timers from game and save them locally"""
        browser = RoboBrowser(history=True, cache=True, parser='lxml', user_agent=self.USERAGENT)
        try:
            browser.open('http://avatar.botva.ru/')

        except ConnectionError:
            print('ConnectionError')
            return False

        try:
            loginform = browser.get_form(action='login.php')
            loginform["email"] = botva_login
            loginform["password"] = botva_pass
            browser.session.headers['Referer'] = 'http://avatar.botva.ru/'
            browser.submit_form(loginform)

        except TypeError:
            if self.check_updateworks(browser):
                browser.session.close()
                return False

        except ConnectionError:
            browser.session.close()
            return False

        browser.open('http://avatar.botva.ru/conflict.php')

        if 'options.php' in browser.url:  # game freeze pers in options.php when it's blocked
            open("need_new_bot", "w").write("need")  # signal to tg bot

            # registration new bot
            from registration import registration
            from settings import name_id
            email = botva_login.replace(str(name_id), str(name_id+1))
            names = ["MrSmith-%s" % str(name_id+1),
                    ]
            with open(bot_dir_path + "settings.py", 'r') as f:
                st = f.read()
                start_login = st.find('\nbotva_login')
                end_login = st.find('\n', start_login+1)

                actual_login = st[start_login:end_login]

                st = st[
                     :start_login+1] + "# " + st[
                                    start_login+1:end_login] + "\n" + "botva_login = " + "'" + email + "'" + st[
                                                                                                            end_login:]
                st = st.replace(f"name_id = {name_id}", f"name_id = {name_id+1}")

            registration(names, email, botva_pass)

            with open(bot_dir_path + "settings.py", 'w') as f:  # write new credentials in settings
                f.write(st)

            return False

        for el in browser.find_all(class_='status1'):

            enemy_part = re.findall(r'data-enemy_id="(\d+)"', str(el))[0]
            our_part = re.findall(r'data-loc_id="(\d+)"', str(el))[0]
            _btl_time = re.findall(r'(\d+):(\d+):(\d+)', str(el))[0]
            
            try:
                dtimer = dt.now().replace(
                    hour=int(_btl_time[0]), 
                    minute=int(_btl_time[1]), 
                    second=int(_btl_time[2])
                    )
            except Exception as e:
                print(f'{dt.now().time()}, error: {e}\n {_btl_time}')
                break
                
            if int(_btl_time[0]) < dt.now().hour:
                dtimer = dtimer + timedelta(1)

            timer = dtimer.timestamp()
            btl_time = ':'.join(_btl_time)

            btl_text = '{} {}/{}'.format(
                    btl_time, 
                    self.part_resurs[int(our_part)-1], 
                    self.part_resurs[int(enemy_part)-1]
                    )

            if btl_text not in self.btl_timers.values() and timer > time.time()+100:
                self.btl_timers[timer] = btl_text

        browser.session.close()

        timers = self.btl_timers.copy()  # del old msgs from base
        for t in timers.keys():
            if time.time() > float(t):
                self.btl_timers.pop(t)
                self.write_btl_to_file()

        return True

    def check(self):
        """Check battles will start soon
        Return message for send"""
        timers = self.btl_timers.copy()
        message = False
        for t in timers.keys():
            if time.time()+100 > float(t):
                message = self.btl_timers[t]
                self.btl_timers.pop(t)
                self.write_btl_to_file()
                
        return message

    def check_updateworks(self, browser=None):
        """return True if updates run on game servers"""
        if not browser:
            browser = RoboBrowser(history=True, cache=True, parser='lxml', user_agent=self.USERAGENT)
            browser.open('http://avatar.botva.ru/')

        text = browser.select
        time = re.findall(r'Ориентировочное время включения - (\d{2}):(\d{2})', str(text))

        if time:
            hour, minute = time[0][0], time[0][1]
            update_time = dt.now().replace(hour=int(hour), minute=int(minute))

            self.update_timer = update_time.timestamp()

            self.btl_timers = {}

            return True

        elif self.update_timer:
            self.update_timer = False

        return False


if __name__ == '__main__':

    LOG_FILENAME = 'btl_parser.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,
                        format=u'%(levelname)-8s [%(asctime)s]  %(message)s')
    logTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    parser = TimerParser()
    try:
        parser.read_btl_file()
    except FileNotFoundError:
        parser.write_btl_to_file()
    timeout = 0

    if parser.update_timer:
        parser.check_updateworks()

    else:
        for _ in range(3):
            parser.parse_timers()

            if parser.btl_timers:
                break
                
            time.sleep(5)

    parser.write_btl_to_file()
