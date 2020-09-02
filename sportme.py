import logging
import random
import time
from datetime import datetime, timedelta
import requests
import urllib3
from tqdm.auto import tqdm

urllib3.disable_warnings()


class SportmeBooker:
    # TODO: научиться передавать забронированные, те что не нужно забронировать
    # поставить счетчик бронирования в цикл бронирования
    #

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.token = None
        self.booked_events = []
        self.all_events = []
        self.dates = None
        self.myaddress = '52'

    def get_token(self):
        """ Авторизуется по логину и паролю и получает токен """

        try:
            s = requests.Session()
            data = {"username": self.login, "password": self.password}
            url = "https://sportme.club/sport/auth/login"
            r = s.post(url, data=data, verify=False)
            request_result = r.json()
            self.token = request_result['token']

            return True
        except Exception as e:
            print(e)
            return False

    def make_rq_url(self, mydate='2020-08-12', ):
        """ Формирует строку для get запроса """

        url = 'https://sportme.club/sport/events/search?zoneId=Europe/Moscow&'
        url += f'objectId={self.myaddress}&cityId=1'
        url += f"&pageSize=10&date={mydate}%2019:00:00&startTime=07:00"
        url += f"&pageNo=1&rand=0.7210804589143462"
        return url

    def get_events_info(self, mydate):
        """Получает список ивентов по определенной дате """

        myurl = self.make_rq_url(mydate=mydate)
        myheaders = {"x-auth-token": self.token}
        res = requests.get(myurl, headers=myheaders, verify=False)
        return res.json()

    def get_all_events(self, only_ids=False):
        """
        Получает список всех ивентов по списку дат
        """

        all_events = []
        for mydate in tqdm(self.dates):
            event_json = self.get_events_info(mydate)

            if event_json['data'].get('newTomorrow'):
                eventlist = event_json['data']['newTomorrow']
                new_eventlist = []
                for el in eventlist:
                    places = el['places']['free']
                    event_id = el['bookId']
                    event_start = el['dateBegin']
                    new_eventlist.append((event_id, event_start, places))
                all_events.extend(new_eventlist)
                time.sleep(1)

        if only_ids:
            all_events = [x[0] for x in all_events]
        self.all_events = all_events
        return True

    def get_morning_events(self):
        """Получает утренние ивенты из списке всех ивентов"""

        morning_events = []
        for el in self.all_events:
            if el[1].split(' ')[1] == '07:00:00':
                morning_events.append(el[0])
        return morning_events

    def get_events_status(self, events):
        """Получает короткую инфо об ивентах"""

        eventids = ','.join([str(x) for x in events])
        url = "https://sportme.club"
        url += f"/sport/events/places?ids={eventids}&rand={random.random()}"
        myheaders = {"x-auth-token": self.token}
        res = requests.get(url, headers=myheaders, verify=False)
        return res.json()

    def check_event_freedom(self, events_status_info):
        """ Проверяет наличие свободных слотов """

        freebookids = []
        for el in events_status_info['data']:
            if el['free'] > 0:
                freebookids.append(el['bookId'])
        if freebookids:
            return freebookids
        else:
            return None

    def check_morning_events(self):
        """ Проверяет наличие свободных мест по утрам """

        self.get_all_events()
        events = self.get_morning_events()
        event_info = self.get_events_status(events)
        result = self.check_event_freedom(event_info)
        return result

    def check_event_booking(self, event_id):
        """Проверяет статус бронирования мероприятия """

        rand = random.random()
        myheaders = {
            "x-auth-token": self.token,
            'authority': 'sportme.club',
            'method': 'POST',
            'path': f'/sport/events/{event_id}/reserve?rand={rand}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'clientwidth': '1615',
            'content-length': '0',
            # 'ip': '185.18.4.94',
            'origin': 'https://sportme.club',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'timezone': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        url = f'https://sportme.club/sport/events/{event_id}/check?rand={rand}'
        try:
            res = requests.put(url, headers=myheaders, verify=False)
            book_status = res.json()
            return book_status
        except Exception as e:
            print(e)
            return False

    def book_event(self, event_id):
        """Бронирует если ивент еще не забронирован"""

        rand = random.random()
        url = f'https://sportme.club/sport/events/{event_id}/reserve?rand={rand}'
        myheaders = {
            "x-auth-token": self.token,
            'authority': 'sportme.club',
            'method': 'POST',
            'path': f'/sport/events/{event_id}/reserve?rand={rand}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'clientwidth': '1615',
            'content-length': '0',
            # 'ip': '185.18.4.94',
            'origin': 'https://sportme.club',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'timezone': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        checker = self.check_event_booking(event_id)
        result = None
        if checker.get('state') == 'OK' or checker.get('message') == 'FINISH_BOOKING':
            try:
                res = requests.post(url, headers=myheaders, verify=False)
                result = res.json()
            except Exception as e:
                print(e)
                logging.info(e)

            if result['state'] == 'OK':
                # print(f'Слот {event_id} забронирован')
                logging.info(f'Слот {event_id} забронирован')
                event_time = self.get_event_time(event_id)
                # print(event_time)
                logging.info(f'Время {event_time}')
                self.booked_events.append(event_id)

                return True
            else:
                logging.info(f'Не получается забронировать {event_id}')
                return None
        else:
            # print('checker не пускает ')
            logging.info('checker не пускает ')
            return None

    def unbook_event(self, event_id):
        """Отменяет бронь по заданному event_id """

        rand = random.random()
        url = f'https://sportme.club/sport/events/{event_id}/unreserve?rand={rand}'
        myheaders = {
            "x-auth-token": self.token,
            'authority': 'sportme.club',
            'method': 'POST',
            'path': f'/sport/events/{event_id}/reserve?rand={rand}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'clientwidth': '1615',
            'content-length': '0',
            'ip': '185.18.4.94',
            'origin': 'https://sportme.club',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'timezone': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.105 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        try:
            res = requests.post(url, headers=myheaders, verify=False)
            result = res.json()
            if result['state'] == 'OK':
                # print(f'Бронирование {event_id} отменено')
                logging.info(f'Бронирование {event_id} отменено')
                self.booked_events.remove(event_id)
                return True
            else:
                # print(f'Не удалось отменить бронь {event_id}')
                logging.info(f'Не удалось отменить бронь {event_id}')
                return False
        except Exception as e:
            print(e)
            return False

    def get_active_bookings(self):
        """Возвращает список забронированных мероприятий """

        rand = random.random()
        url = f'https://sportme.club/sport/events/wow?rand={rand}'
        myheaders = {
            "x-auth-token": self.token,
            'authority': 'sportme.club',
            'method': 'POST',
            'path': f'/sport/events/wow?rand={rand}',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'clientwidth': '1615',
            'content-length': '0',
            'origin': 'https://sportme.club',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'timezone': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        try:
            res = requests.get(url, headers=myheaders, verify=False)
            result = res.json()
            active_bookings = []
            for el in result['data']:
                if el['state'] == 'active':
                    active_bookings.append(el['bookId'])
            self.booked_events = active_bookings
            return True
        except Exception as e:
            print(e)
            return False

    def get_event_time(self, event_id):
        """Возвращает дату и время события по идентификатору """

        res = [None, None]
        for el in self.all_events:
            if el[0] == event_id:
                res = el

        return res[1]

    def run(self, routine_name='morning'):
        """Запускает процедуру"""
        self.get_token()

        if routine_name == 'morning':
            c = 0
            while True:
                if c % 100 == 0:
                    print(f'Цикл {c} работаем...')

                self.morning_routine()
                c += 1
                if len(self.booked_events) >= 4:
                    print("Дело сделано")
                    break

    def get_dates(self, num_days=10):
        """Содает список дата на num_days вперед """

        datetimes = [datetime.today() + timedelta(days=i) for i in range(-1, num_days)]
        dates = [x.strftime('%Y-%m-%d') for x in datetimes]
        self.dates = dates

        return True

    def morning_routine(self):
        """Процедура бронирования утренних слотов"""

        self.get_dates()
        self.get_active_bookings()
        free_bookids = self.check_morning_events()
        if free_bookids:
            for event_id in free_bookids:
                if event_id not in self.booked_events:
                    b_result = self.book_event(event_id)
                    if b_result:
                        self.booked_events.append(event_id)
                    time.sleep(1)
        time.sleep(30)
