import requests
import timeit
import threading

payload = {'gas_needed': '10000', 'tx_speed': 'medium', 'public_address': '0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d'}

#for i in range(10000):
#    start = timeit.default_timer()
#    r = requests.get('http://localhost:8000/fill-wallet-for-gas', params=payload)
#    #print(r.json())
#    stop = timeit.default_timer()
#    print('Time: ', stop - start)



def blockreq():
    start = timeit.default_timer()
    r = requests.get('http://api.digitpay.de/fill-wallet-for-gas', params=payload)
    print(r.json())
    stop = timeit.default_timer()
    print('Time: ', stop - start)






i = 1

def set_interval(func, sec):
    def func_wrapper():
        #++sec
        #print(sec)
        set_interval(func, sec)
        func()
    #++sec
    #print(sec)
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

set_interval(blockreq,10)


