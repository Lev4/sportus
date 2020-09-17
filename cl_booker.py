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
