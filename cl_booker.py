import sys
import logging
from sportme import SportmeBooker
from localconfig import logindata, sportmetoken, chatid


def main():
    """
    python3 cl_booker.py -e mail
    """
    account = None
    routine = None
    if len(sys.argv) > 1:
        routine = sys.argv[1]
        account = sys.argv[2]

    else:
        msg = 'Не заданы параметры. Заканчиваю работу!'
        logging.info(msg)
        print(msg)
        exit()

    if account not in logindata.keys():
        msg = "Такой учетной записи нет"
        logging.info(msg)
        print(msg)
        exit()

    if routine == "-m":
        routine_par = 'morning'
        sp = SportmeBooker(logindata, account)
        sp.send_message(chatid, sportmetoken, f'Начинаю работу под учеткой {sp.account}')
        sp.run(routine_par)

    elif routine == "-e":
        routine_par = 'evening'
        sp = SportmeBooker(logindata, account)
        sp.send_message(chatid, sportmetoken, f'Начинаю работу под учеткой {sp.account}')
        sp.run(routine_par)

    else:
        logging.info("Неправильный первый аргумент -  должен быть -m либо -e ")
        exit()


if __name__ == '__main__':
    main()
