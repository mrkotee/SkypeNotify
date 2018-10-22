from battle_parser import TimerParser
from seleskypesender import SkypeSender
import time
from settings import skype_login, skype_pass, skype_groups

skypesender = SkypeSender()
skypesender.login(skype_login, skype_pass)
chat_grops = skype_groups

skype_admin = 'MrKotee ev'
skypesender.select_chat(skype_admin)
skypesender.send_message('start')

parser = TimerParser()
# timeout = 0
# while True:
#     if parser.update_timer:
#         timer = parser.update_timer - time.time()
#         if timer < 0:
#             timer = 180
#         time.sleep(timer)
#         parser.check_updateworks()

#     else:
#         if time.time() > timeout:
#             timeout = time.time() + 600

#             if not parser.parse_timers():
#                 continue

#         msg = parser.check()
#         if msg:
#             for chat in chat_grops:
#                 skypesender.select_chat(chat)
#                 skypesender.send_message(msg)

#         time.sleep(10)

update_time = 0
updates_msg_sended = False
zero_btl_count = 0
while True:
    if update_time < time.time():
        parser.read_btl_file()
        if update_time == 0:
            skypesender.select_chat(skype_admin)
            skypesender.send_message('{} battles in base'.format(len(parser.btl_timers)))
            skypesender.select_chat(chat_grops[0])

        update_time = time.time() + 720
        if time.gmtime(time.time()).tm_hour == 20:
            skypesender.select_chat(skype_admin)
            skypesender.send_message('still working\n{} battles in base'.format(len(parser.btl_timers)))
            skypesender.select_chat(chat_grops[0])

        if len(parser.btl_timers) == 0:
            zero_btl_count += 1
            if zero_btl_count > 6:
                skypesender.select_chat(skype_admin)
                skypesender.send_message('none battle found last 6 times!')

    msg = parser.check()
    if msg:
        for chat in chat_grops:
            skypesender.select_chat(chat)
            skypesender.send_message(msg)

    if parser.update_timer:
        if not updates_msg_sended:
            skypesender.select_chat(skype_admin)
            skypesender.send_message('updates!')
            updates_msg_sended = True

            timer = parser.update_timer - time.time()
            if timer < 0:
                timer = 180
            time.sleep(timer)

    elif updates_msg_sended:
        skypesender.select_chat(skype_admin)
        skypesender.send_message('updates ended!')
        updates_msg_sended = False
        skypesender.select_chat(chat_grops[0])


    time.sleep(10)
