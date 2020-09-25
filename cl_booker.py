from sportme import SportmeBooker
from localconfig import logindata, sportmetoken, chatid





def main():
    sp = SportmeBooker(logindata, 'mail')
    sp.send_message(chatid, sportmetoken, f'Начинаю работу под учеткой {sp.account}')
    sp.run('morning')
    sp.send_message(chatid, sportmetoken, f'Забронированы следующие слоты {",".join(sp.booked_events)}')
    sp.send_message(chatid, sportmetoken, f'Завершаю работу под учеткой {sp.account}')
    booked_events = sp.booked_events

    sp = SportmeBooker(logindata, 'inbox', booked_events)
    sp.send_message(chatid, sportmetoken, f'Начинаю работу под учеткой {sp.account}')
    sp.run('morning')
    sp.send_message(chatid, sportmetoken, f'Забронированы следующие слоты {",".join(sp.booked_events)}')
    sp.send_message(chatid, sportmetoken, f'Завершаю работу под учеткой {sp.account}')


if __name__ == '__main__':
    main()




# Traceback (most recent call last):
#   File "cl_booker.py", line 24, in <module>
#     main()
#   File "cl_booker.py", line 11, in main
#     sp.run('morning')
#   File "/root/sportus/sportme.py", line 315, in run
#     self.morning_routine()
#   File "/root/sportus/sportme.py", line 335, in morning_routine
#     free_bookids = self.check_morning_events()
#   File "/root/sportus/sportme.py", line 126, in check_morning_events
#     result = self.check_event_freedom(event_info)
#   File "/root/sportus/sportme.py", line 112, in check_event_freedom
#     for el in events_status_info['data']:
# KeyError: 'data'