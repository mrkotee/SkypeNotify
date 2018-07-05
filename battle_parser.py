import re, time
from robobrowser import RoboBrowser
from datetime import datetime as dt
from settings import botva_pass, botva_login


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

    def parse_timers(self):
        browser = RoboBrowser(history=True, cache=True, user_agent=self.USERAGENT)
        browser.open('http://avatar.botva.ru/')

        loginform = browser.get_form(action='login.php')
        loginform["email"] = botva_login
        loginform["password"] = botva_pass
        browser.session.headers['Referer'] = 'http://avatar.botva.ru/'
        browser.submit_form(loginform)

        browser.open('http://avatar.botva.ru/conflict.php')

        for el in browser.find_all(class_='status1'):
            enemy_part = re.findall(r'data-enemy_id="(\d+)"', str(el))[0]
            our_part = re.findall(r'data-loc_id="(\d+)"', str(el))[0]
            _btl_time = re.findall(r'(\d+):(\d+):(\d+)', str(el))[0]
            try:
                dtimer = dt.now().replace(
                	hour=int(_btl_time[0]), 
                	minute=int(_btl_time[1]), 
                	second=int(_btl_time[2])-3
                	)
            except:
                print(_btl_time)
            if int(_btl_time[0]) < dt.now().hour:
                dtimer.replace(day=dt.now().day+1)
            timer = dtimer.timestamp()
            btl_time = ':'.join(_btl_time)

            btl_text = '{} {}/{}'.format(
                    btl_time, 
                    self.part_resurs[int(our_part)-1], 
                    self.part_resurs[int(enemy_part)-1]
                    )
            if btl_text not in self.btl_timers.values():
                self.btl_timers[timer] = btl_text

        browser.session.close()

    def check(self):
        timers = self.btl_timers.copy()
        message = False
        for t in timers.keys():
            if time.time()+100 > t:
                print('*'*50)
                print(self.btl_timers[t])
                message = self.btl_timers[t]
                self.btl_timers.pop(t)
                print(dt.now().time())
                print(self.btl_timers)
                print('*'*50)
        return message


if __name__ == '__main__':
    parser = TimerParser()
    timeout = 0
    while True:
        if time.time() > timeout:
            parser.parse_timers()
            # timeout = time.time() + 600
            timeout = time.time() + 100

        # сделать проверку ключа в словаре!
        parser.check()

        time.sleep(10)
