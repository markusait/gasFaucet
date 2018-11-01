import os
from web3 import Web3, HTTPProvider, middleware
from web3.contract import ConciseContract
from web3.auto import w3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware.cache import construct_simple_cache_middleware
from cachetools import TTLCache, cachedmethod, cached, LRUCache
from functools import partial
from cachetools.keys import hashkey
import functools
import threading
import cachetools.func


#import timeit
#start = timeit.default_timer()

w3.eth.enable_unaudited_features()
token = os.environ['INFURA_TOKEN']
url = "https://mainnet.infura.io/%s" % token
w3 = Web3(Web3.HTTPProvider(url))
#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
#setting ttl to < 0.000001 will show the effect
#cache = TTLCache(maxsize=10000, ttl=60)
#cache = LRUCache(maxsize=10000)


def testBool(method,params,response):
        return True

block_hash_cache_middleware = construct_simple_cache_middleware(
       # default sample size of gas price strategies is 120
       cache_class=functools.partial(LRUCache, 150),
       rpc_whitelist='eth_getBlockByHash',
       should_cache_fn=testBool
)

w3.middleware_stack.add(block_hash_cache_middleware)









#@cached(cache, key=partial(hashkey, 'gas'))
def calcEthNeeded(gasNeeded, speed):
   if speed == 'fast':
       w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
       gasPrice = w3.eth.generateGasPrice()
       print(gasPrice)
       return (gasPrice * gasNeeded) /  (10 ** 9)
   if speed =='medium':
       w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
       gasPrice = w3.eth.generateGasPrice()
       print(gasPrice)
       return (gasPrice * gasNeeded) /  (10 ** 9)
   if speed == 'slow':
       w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
       gasPrice = w3.eth.generateGasPrice()
       print(gasPrice)
       return (gasPrice * gasNeeded) /  (10 ** 9)





def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        print(func(1000, 'fast'))
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

#initializing
#calcEthNeeded(1000,'fast')
#set_interval(calcEthNeeded,10)








#print(calcEthNeeded(10000,'fast'))
#stop = timeit.default_timer()
#print('Time: ', stop - start)
