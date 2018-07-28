from battle_parser import TimerParser
from seleskypesender import SkypeSender
import time
from settings import skype_login, skype_pass, skype_groups

skypesender = SkypeSender()
skypesender.login(skype_login, skype_pass)
chat_grops = skype_groups

# skypesender.select_chat('Будильник')
# skypesender.send_message('start')

parser = TimerParser()
timeout = 0
while True:
    if parser.update_timer:
        timer = parser.update_timer - time.time()
        time.sleep(timer)
        parser.check_updateworks()

    else:
        if time.time() > timeout:
            if not parser.parse_timers():
                continue
                
            timeout = time.time() + 600
            # timeout = time.time() + 100

        msg = parser.check()
        if msg:
            for chat in chat_grops:
                skypesender.select_chat(chat)
                skypesender.send_message(msg)

        time.sleep(10)