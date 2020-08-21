from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import time

# username = 'rs31@inbox.ru'
# password = 'ALEX12345'


class SportmeBookerSelenium:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = None

    def start_and_login_sportme(self):
        self.browser = webdriver.Chrome('driver/chromedriver')
        self.browser.get('https://www.sportme.club')
        self.browser.maximize_window()
        status = False
        try:
            elementID = self.browser.find_element_by_id('link_login')
            elementID.click()
            time.sleep(1)
            elementID = self.browser.find_element_by_id('email')
            elementID.send_keys(username)
            elementID = self.browser.find_element_by_id('password')
            elementID.send_keys(password)
            elementID.submit()
            time.sleep(1)
            status = True
        except:
            print("Что-то пошло не так")
        finally:
            return status

    def make_url(self, mydate, myaddress="1", myhour='07'):
        """Собираем url
         myaddress="1" Волгоградский проспект
         myaddress = "52" Кутузовский проспект
        """

        #     myhour= datetime.now().strftime("%H")
        mytime = f"{myhour}:00"
        url = "https://sportme.club/list?"
        url += f"date={mydate}&"
        url += f"time={mytime}&"
        url += f"city=1&address={myaddress}&pageNo=1&changed=true"
        return url

    def check_oops(self):
        """ Проверка наличия слотов """

        res = None
        status = False
        try:
            elementID = self.browser.find_element_by_css_selector("h1.content_h1.txt_blue.txt_align_center")
            res = elementID.get_attribute('innerHTML')
            # print(res)
            if res == 'Oops! НЕОЖИДАННО!':
                status = True
        except:
            print("Слоты открыты")
        finally:
            return status

    def book_first(self):
        """ Находим розовую кнопку и нажимаем -забронировать- """

        status = False
        elementID = self.browser.find_elements_by_css_selector('button.btn.pink')
        for el in elementID:
            page = el.get_attribute('innerHTML')
            soup = BeautifulSoup(page)
            #         print(soup.text)
            if soup.text == 'Забронировать':
                el.click()
                print("Слот выбран")
                status = True
                break
            else:
                print('Нет возможности забронировать слот')
        return status

    def confirm_booking(self, browser):
        """Подтверждаем бронирование """

        status = False
        try:
            elementID = browser.find_elements_by_css_selector("div.col.xs-col")
            if len(elementID) > 0:
                elementID[1].click()
                status = True
        except:
            print('что-то пошло не так')
        finally:
            return status

    def click_ok(self, browser):
        """Нажимаем ОК"""

        status = False
        try:
            elementID = browser.find_element_by_id("button_notification")
            elementID.click()
            status = True
        except:
            print('Нет кнопки ОК')
        # elementID.get_attribute('innerHTML')
        finally:
            return status
