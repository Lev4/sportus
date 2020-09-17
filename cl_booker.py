from sportme import SportmeBooker
from localconfig import logindata


def main():
    login = logindata['mail']['username']
    password = logindata['mail']['password']

    sp = SportmeBooker(login, password)
    sp.run('morning')

    login = logindata['inbox']['username']
    password = logindata['inbox']['password']

    sp = SportmeBooker(login, password)
    sp.run('morning')


if __name__ == '__main__':
    main()
