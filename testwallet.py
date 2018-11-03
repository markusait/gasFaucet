from web3.auto import w3
import os
import functools
from cachetools import TTLCache, cachedmethod, LRUCache
from json.decoder import JSONDecodeError
from web3 import Web3, HTTPProvider, middleware
from web3 import middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy

from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware.cache import construct_simple_cache_middleware
from web3.middleware import geth_poa_middleware
from functools import partial
from cachetools import cached, LRUCache
from cachetools.keys import hashkey
import cachetools.func

#w3.middleware_stack.add(middleware.time_based_cache_middleware)
#w3.middleware_stack.add(middleware.latest_block_based_cache_middleware)
#w3.middleware_stack.add(middleware.simple_cache_middleware)

w3.eth.enable_unaudited_features()
token = os.environ['INFURA_TOKEN']
url = "https://ropsten.infura.io/%s" % token
#url = "http://127.0.0.1:8545"
w3 = Web3(Web3.HTTPProvider(url))

def testBool(method,params,response):
	return True

block_hash_cache_middleware = construct_simple_cache_middleware(
      # default sample size of gas price strategies is 120
      cache_class=functools.partial(LRUCache, 150),
      rpc_whitelist='eth_getBlockByHashs',
      should_cache_fn=testBool
 )

w3.middleware_stack.add(block_hash_cache_middleware)






#connection_test_middleware = make_connection_test_middleware()

#cache = LRUCache(maxsize=10000)
#cache = TTLCache(maxsize=10000, ttl=0.0000000000001)



#@cached(cache, key=partial(hashkey, 'gas'))
#@cachetools.func.ttl_cache(maxsize=64, ttl=300)
def gas_price():
        print('recived')
        gasPrice =  w3.eth.generateGasPrice()
        return gasPrice
for i in range(0,50):
    w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
    print('slow:' ,gas_price())
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
    print("medium:", gas_price())
    w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
    print("fast:", gas_price())




#w3.middleware_stack.inject(connection_test_middleware, layer=0)


#w3.eth.setGasPriceStrategy(rpc_gas_price_strategy)
#w3.middleware_stack.inject(geth_poa_middleware, layer=0)
#w3.middleware_stack.add(middleware.time_based_cache_middleware)
#print('RPC:', w3.eth.generateGasPrice())
#w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
#w3.middleware_stack.add(middleware.time_based_cache_middleware)
#print('Slow', w3.eth.generateGasPrice())
#w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
#print('Medium:', w3.eth.generateGasPrice())
#w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
#print('Fast:', w3.eth.generateGasPrice())
