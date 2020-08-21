from sportme import SportmeBooker
from localconfig import logindata

login = logindata['inbox']['username']
password = logindata['inbox']['password']


sp = SportmeBooker(login, password)


if __name__ == '__main__':
    sp.run('morning')
