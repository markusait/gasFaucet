from config import ETH_PRIVATE_KEY, ROPSTEN_URL, MAINNET_URL
from web3 import Web3, HTTPProvider, middleware
from web3.auto import w3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware.cache import construct_simple_cache_middleware
from eth_account import Account
from cachetools import LRUCache, Cache
from functools import partial
from threading import Timer
import timeit

cacheInterval = 30
blocksToCache = 150
#connection to node
w3 = Web3(Web3.HTTPProvider(ROPSTEN_URL))
#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

#adding caching middle ware with LRU Cache and 150 items
block_hash_cache_middleware = construct_simple_cache_middleware(
       cache_class=partial(LRUCache, blocksToCache),
       rpc_whitelist='eth_getBlockByHash',
)
w3.middleware_stack.add(block_hash_cache_middleware)

#Account initalization with priavte Key
acct = Account.privateKeyToAccount(ETH_PRIVATE_KEY)


#Cache with 3 categories fast, medium ,slow
priceCache = Cache(maxsize=3)

#making sure the gas Price can be calculated quickly at any time
def keepCacheWarm():
    start = timeit.default_timer()

    w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
    priceCache.__setitem__('fast',w3.eth.generateGasPrice())

    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
    priceCache.__setitem__('medium',w3.eth.generateGasPrice())

    w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
    priceCache.__setitem__('slow',w3.eth.generateGasPrice())

    stop = timeit.default_timer()
    print('Time: ', stop - start)
    print(priceCache.__getitem__('fast'))
    print(priceCache.__getitem__('medium'))
    print(priceCache.__getitem__('slow'))
    Timer(cacheInterval, keepCacheWarm).start()

#Timer(cacheInterval, keepCacheWarm).start()
#keepCacheWarm()


#takes in the requested eth in wei and returns txHash
def sendTransaction(gasNeeded, speed, receiver):
    #calculating the gasPrice
    gasPrice = priceCache.__getitem__(speed)
    ethNeeded = gasPrice * gasNeeded
    #TODO: increment manually after each call for quicker transactions
    nonce=w3.eth.getTransactionCount(acct.address, 'pending')
    txGasPrice = 20000000000

    transaction = {
        'to': receiver,
        'value': ethNeeded,
        'gas': 314150,
        'gasPrice': txGasPrice,
        'nonce': nonce,
        'data': '53656e742066726f6d20676173466175636574202a2e2a',
        'chainId': 3, # Ropsten chain ID
        }
    try:
        signed = Account.signTransaction(transaction, acct.privateKey)
        gweiGasPrice = "%.2f" % (gasPrice / 10 ** 9)
        txHash = (w3.eth.sendRawTransaction(signed.rawTransaction)).hex()
        return {"message": "successful",  "txHash":txHash,"gasPrice in Gwei": gweiGasPrice,"Eth sent in Wei":ethNeeded, "link": "https://ropsten.etherscan.io/tx/" + txHash}
    except:
        return {"message":"I am not ready yet"}

