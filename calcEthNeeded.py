from web3 import Web3, HTTPProvider, middleware
from web3.contract import ConciseContract
from web3.auto import w3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy
from web3.gas_strategies.rpc import rpc_gas_price_strategy
 
 
#print(rpc_gas_price_strategy(we3))
 
 
#import timeit
#start = timeit.default_timer()
 
w3.eth.enable_unaudited_features()
 
we3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/3cad50878c924727bcc2cc0fb99cf3960"))
#we3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
we3.eth.enable_unaudited_features()

#we3.middleware_stack.inject(geth_poa_middleware, layer=0)
we3.middleware_stack.add(middleware.time_based_cache_middleware)
#we3.middleware_stack.add(middleware.latest_block_based_cache_middleware)
#we3.middleware_stack.add(middleware.simple_cache_middleware)


def calcEthNeeded(gasNeeded, speed):
   if speed == 'fast':
       we3.eth.setGasPriceStrategy(fast_gas_price_strategy)
       gasPrice = we3.eth.generateGasPrice()
       return (gasPrice * gasNeeded) /  (10 ** 9)
   if speed =='medium':
       we3.eth.setGasPriceStrategy(medium_gas_price_strategy)
       gasPrice = we3.eth.generateGasPrice()
       return (gasPrice * gasNeeded) /  (10 ** 9)
   if speed == 'slow':
       we3.eth.setGasPriceStrategy(slow_gas_price_strategy)
       gasPrice = we3.eth.generateGasPrice()
       return (gasPrice * gasNeeded) /  (10 ** 9)

print(calcEthNeeded(10000,'medium'))
#stop = timeit.default_timer()
#print('Time: ', stop - start)

