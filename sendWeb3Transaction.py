from config import ETH_PRIVATE_KEY, ROPSTEN_URL, MAINNET_URL
from web3 import Web3, HTTPProvider, middleware
from web3.auto import w3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware.cache import construct_simple_cache_middleware
from eth_account import Account
from cachetools import LRUCache
from functools import partial
from threading import Timer
#connection to node
w3 = Web3(Web3.HTTPProvider(ROPSTEN_URL))
#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


#adding caching middle ware with LRU Cache and 150 items
block_hash_cache_middleware = construct_simple_cache_middleware(
       cache_class=partial(LRUCache, 150),
       rpc_whitelist='eth_getBlockByHash',
)
w3.middleware_stack.add(block_hash_cache_middleware)

#Account initalization with priavte Key
acct = Account.privateKeyToAccount(ETH_PRIVATE_KEY)


#calculates Gas Price for a given speed parameter
def calcGasPrice(speed):
   if speed == 'fast':
       w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
       gasPrice = w3.eth.generateGasPrice()
       print(gasPrice)
       return gasPrice
   if speed =='medium':
       w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
       gasPrice = w3.eth.generateGasPrice()
       print(gasPrice)
       return gasPrice
   if speed == 'slow':
       w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
       gasPrice = w3.eth.generateGasPrice()
       print(gasPrice)
       return gasPrice



#takes in the requested eth in wei and returns txHash
def sendTransaction(gasNeeded, speed, receiver):
    #calculating the gasPrice
    gasPrice=calcGasPrice(speed)
    ethNeeded = gasPrice * gasNeeded
    #TODO: increment manually after each call for quicker transactions
    nonce=w3.eth.getTransactionCount(acct.address, 'pending')

    transaction = {
        'to': receiver,
        'value': ethNeeded,
        'gas': 314150,
        'gasPrice': calcGasPrice('fast'),
        'nonce': nonce,
        'data': '53656e742066726f6d20676173466175636574202a2e2a',
        'chainId': 3, # Ropsten chain ID
        }

    signed = Account.signTransaction(transaction, acct.privateKey)
    gweiGasPrice = "%.2f" % (gasPrice / 10 ** 9)
    try:
        txHash = (w3.eth.sendRawTransaction(signed.rawTransaction)).hex()
        return {"message": "successful",  "txHash":txHash,"gasPrice in Gwei": gweiGasPrice,"Eth sent in Wei":ethNeeded, "link": "https://ropsten.etherscan.io/tx/" + txHash}
    except:
        return {"message":"I am notready yet"}
        #sendTransaction(gasNeeded, speed, receiver)

#making sure the gas Price can be calculated quickly at any time
def keepCacheWarm():
    Timer(60, keepCacheWarm).start()
    calcGasPrice('fast')

keepCacheWarm()
#print(sendTransaction(10000,'fast','0xF0109fC8DF283027b6285cc889F5aA624EaC1F55'))
