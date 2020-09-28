from sportme import SportmeBooker
from localconfig import logindata, sportmetoken, chatid





def main():

    sp = SportmeBooker(logindata, 'inbox')
    sp.send_message(chatid, sportmetoken, f'Начинаю работу под учеткой {sp.account}')
    # sp.run('morning')
    sp.run('evening')
    sp.send_message(chatid, sportmetoken, f'Забронированы следующие слоты {",".join([str(x) for x in sp.booked_events])}')
    sp.send_message(chatid, sportmetoken, f'Завершаю работу под учеткой {sp.account}')


if __name__ == '__main__':
    main()




