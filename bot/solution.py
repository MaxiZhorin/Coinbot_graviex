# -*- coding: utf-8 -*-
import random
import time
import numpy as np
import urllib2
import json
import hmac
import hashlib
import urllib
from decimal import Decimal
import ssl


# юрл биржи
BASE_URL = 'https://graviex.net'

class Auth():
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def urlencode(self, params):
        keys = params.keys()
        keys.sort()
        query = ''
        for key in keys:
            value = params[key]
            if key != "orders":
                query = "%s&%s=%s" % (query, key, value) if len(query) else "%s=%s" % (key, value)
            else:
                d = {key: params[key]}
                for v in value:
                    ks = v.keys()
                    ks.sort()
                    for k in ks:
                        item = "orders[][%s]=%s" % (k, v[k])
                        query = "%s&%s" % (query, item) if len(query) else "%s" % item
        return query

    def sign(self, verb, path, params=None):
        query = self.urlencode(params)
        msg = "|".join([verb, path, query])
        signature = hmac.new(self.secret_key, msg=msg, digestmod=hashlib.sha256).hexdigest()
        return signature

    def sign_params(self, verb, path, params=None):
        if not params:
            params = {}
        params.update({'tonce': int(1000*time.time()), 'access_key': self.access_key})
        query = self.urlencode(params)
        signature = self.sign(verb, path, params)
        return signature, query

API_BASE_PATH = '/api/v2'
API_PATH_DICT = {
    # GET
    'members': '%s/members/me.json',
    'markets': '%s/markets.json',
    'tickers' : '%s/tickers/%%s.json',
    'orders': '%s/orders.json',
    'order': '%s/order.json',
    'order_book': '%s/order_book.json',
    'trades': '%s/trades.json',
    'my_trades': '%s/trades/my.json',
    'k': '%s/k.json',
    'clear': '%s/orders/clear.json',
    'delete_order': '%s/order/delete.json',
    'multi_orders': '%s/orders/multi.json',
}

def get_api_path(name):
    path_pattern = API_PATH_DICT[name]
    return path_pattern % API_BASE_PATH

class Client():

    def __init__(self, access_key=None, secret_key=None):
        if access_key and secret_key:
            self.auth = Auth(access_key, secret_key)


    def get(self, path, params=None):
        verb = "GET"
        signature, query = self.auth.sign_params(verb, path, params)
        url = "%s%s?%s&signature=%s" % (BASE_URL, path, query, signature)
        resp = urllib2.urlopen(url)
        data = resp.readlines()
        if len(data):
            return json.loads(data[0])

    def post(self, path, params=None):
        verb = "POST"
        signature, query = self.auth.sign_params(verb, path, params)
        url = "%s%s" % (BASE_URL, path)
        data = "%s&signature=%s" % (query, signature)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        resp = urllib2.urlopen(url, data,context=ctx)
        data = resp.readlines()
        if len(data):
            return json.loads(data[0])

# апи токен и серкрет токен
client = Client(access_key='z81oksjCIVYdZqOnS79c4qnCbY7T9oYc0x4qNF3s', secret_key='mft9K1Ks02oMabnzIaanYRIuZq0HVkLIe0IYMWYs')

def order_price_act():
    orders = client.get(get_api_path('order_book'), params={'market': order_market})
    orders_sell = orders['asks']
    for i in orders_sell:
        print i
        price_for_orders = float(i['price'].encode('utf-8'))
        price_for_orders = "{:.9f}".format(price_for_orders)
        return price_for_orders


def order_value():
    orders = client.get(get_api_path('order_book'), params={'market': order_market})
    orders_sell = orders['asks']
    for i in orders_sell:
        print 'valvalva',i
        order_volume = str(i['remaining_volume'].encode('utf-8'))
        return order_volume
def clear_orders():
    for i in order_clear:
        params = {"id": i}
        res = client.post(get_api_path('delete_order'), params)
    order_clear[:] = []

def price_orders():
    orders = client.get(get_api_path('order_book'), params={'market': order_market})
    orders_sell = orders['asks']
    for i in orders_sell:
        price_for_orders = float(i['price'].encode('utf-8'))
        price_for_orders = Decimal(price_for_orders - random.uniform(min_way, max_way))
        price_for_orders = "{:.9f}".format(price_for_orders)
        return price_for_orders

def price_orders_new():
    orders = client.get(get_api_path('order_book'), params={'market': order_market})
    orders_sell = orders['asks']
    for i in orders_sell:
        price_for_orders = float(i['price'].encode('utf-8'))
        price_for_orders = Decimal(price_for_orders + way2)
        price_for_orders = "{:.9f}".format(price_for_orders)
        return price_for_orders


def price_random(order_price_min,order_price_max):
    order_price = random.uniform(order_price_min,order_price_max)
    order_price = round(order_price,4)
    return order_price



order_clear = list()
markets =  client.get(get_api_path('markets'))

#####################################################

# настройки задержки покупки ордеров
time_order_min = 5
time_order_max = 10
# настройки объема создания ордера
buy_value_min = 300
buy_value_max = 340
# настройки объема ордера
order_price_min = 30
order_price_max = 40
# валютная пара
order_market = str('menbtc')

# процент создания второго ордера

percent = 0.3

# шаг создания ордера 1
min_way = 0.000000002
max_way = 0.000000006
# шаг создания 2 ордера
way2 = 0.000000001

######################################################

orders = client.get(get_api_path('order_book'), params={'market': order_market})
orders_sell = orders['asks']
print orders_sell
while True:
    print 'zero zero zero'
    buy_value = random.randint(buy_value_min, buy_value_max)
    origin_value = buy_value * percent # 30%
    clear_orders()  # очищает ордера
    time_order = random.randint(time_order_min, time_order_max)
    price_for_orders = price_orders()
    params = {'market': order_market, 'side': 'sell', 'volume': buy_value, 'price': price_for_orders}
    res = client.post(get_api_path('orders'), params)
    order_id = int(res['id'])
    order_clear.append(order_id)
    print buy_value
    time.sleep(time_order)
    while buy_value>0:
        print 'ok0'
        order_act = order_price_act() # актуальная цена рынка
        order_val = order_value() # актуальный объем
        order_val2 =str(float(buy_value))
        if str(order_act) == str(price_for_orders):
            print 'ok1',order_val,order_val2
            if order_val == order_val2:
                print 'ok2'
                order_price = price_random(order_price_min,order_price_max)
                if order_price < buy_value:
                    if origin_value >= float(buy_value):
                        print '30%'
                        buy_value_new = random.randint(buy_value_min, buy_value_max)
                        time_order = random.randint(time_order_min, time_order_max)
                        price_for_orders_new = price_orders_new()
                        params = {'market': order_market, 'side': 'sell', 'volume': buy_value_new, 'price': price_for_orders_new}
                        res = client.post(get_api_path('orders'), params)
                        order_id = int(res['id'])
                        order_clear.append(order_id)
                        print res
                        origin_value = 0
                    print 'ok3'
                    params = {'market': order_market, 'side': 'buy', 'volume': order_price, 'price': price_for_orders}
                    res = client.post(get_api_path('orders'), params)
                    buy_value = buy_value - order_price
                    time.sleep(time_order)
                else:
                    print 'ok4'
                    order_price = buy_value
                    params = {'market': order_market, 'side': 'buy', 'volume': order_price, 'price': price_for_orders}
                    res = client.post(get_api_path('orders'), params)
                    time.sleep(time_order)

                    buy_value = buy_value_new
                    origin_value = buy_value_new * percent  # 30%
                    price_for_orders = price_for_orders_new
                    time.sleep(time_order)
            else:
                print 'break'
                break
        else:
            break

