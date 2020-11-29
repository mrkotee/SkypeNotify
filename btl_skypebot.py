from battle_parser import TimerParser
from seleskypesender import SkypeSender
import time
from settings import skype_login, skype_pass, skype_groups


def main():
    skypesender = SkypeSender()
    try:
        skypesender.login(skype_login, skype_pass)
    except:
        open("need_new_bot", "w").write("need")
        return False

    chat_grops = skype_groups

    skype_admin = 'MrKotee ev'
    skypesender.select_chat(skype_admin)
    skypesender.send_message('start')

    parser = TimerParser()

    update_time = 0
    updates_msg_sended = False
    zero_btl_count = 0
    upd_notify = 0
    prev_upd_time = 0
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
            elif zero_btl_count:
                zero_btl_count = 0

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


            if upd_notify != parser.update_timer:
                upd_notify = parser.update_timer

                upd_time = time.gmtime(parser.update_timer)
                if upd_time != prev_upd_time:
                    prev_upd_time = upd_time
                    
                    mnts_to_str = lambda mnts: '0'+str(mnts) if mnts < 10 else mnts
                    msg_text = "Ориентировочное время включения {}:{}".format(
                        upd_time.tm_hour + 3, 
                        mnts_to_str(upd_time.tm_min)
                        )
                    
                    skypesender.select_chat(skype_admin)
                    skypesender.send_message(msg_text)

                    for chat in chat_grops:
                        skypesender.select_chat(chat)
                        skypesender.send_message(msg_text)

        elif updates_msg_sended:
            skypesender.select_chat(skype_admin)
            skypesender.send_message('updates ended!')
            updates_msg_sended = False
            skypesender.select_chat(chat_grops[0])

            # for chat in chat_grops:
            #     skypesender.select_chat(chat)
            #     skypesender.send_message(msg_text)

        time.sleep(10)


main()
