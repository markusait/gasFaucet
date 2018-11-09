import requests
import timeit
import threading
from random import randint
import json

payload = [{'gas_needed': 1, 'tx_speed': 'fast', 'public_address': '0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d'}, {'gas_needed': 1, 'tx_speed': 'medium', 'public_address': '0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d'}, {'gas_needed': 1, 'tx_speed': 'slow', 'public_address':'0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d'}]


def blockreq():
    start = timeit.default_timer()
    r = requests.get('http://localhost:8000/fill-wallet-for-gas', params=payload[randint(0,2)])
    #r = requests.get('http://api.digitpay.de/fill-wallet-for-gas', params=payload[randint(0,2)])
    getNonce()
    print(r.json())
    stop = timeit.default_timer()
    print('Time: ', stop - start)


def getNonce():
    headers = {'Content-type': 'application/json'}
    url = 'http://localhost:8545'
    data = {"method":"parity_nextNonce","params":["0x160A53C6f8B82F8D5e2B77acfD0aED85116fC512"],"id":1,"jsonrpc":"2.0"}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.json()['result'])

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

set_interval(blockreq,2)
#getNonce()

