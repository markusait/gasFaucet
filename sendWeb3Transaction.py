from config import ETH_PRIVATE_KEY, ROPSTEN_URL, MAINNET_URL
from web3 import Web3, HTTPProvider, middleware
from web3.auto import w3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3.middleware.cache import construct_simple_cache_middleware
from eth_account import Account
from eth_utils import is_hex_address
from cachetools import LRUCache, Cache
from functools import partial
from threading import Timer
import timeit


#connection to node
#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider(ROPSTEN_URL))

cacheInterval = 30



blocksToCache = 150
# adding caching middle ware with LRU Cache and 150 items
block_hash_cache_middleware = construct_simple_cache_middleware(
    cache_class=partial(LRUCache, blocksToCache),
    rpc_whitelist='eth_getBlockByHash'
)
w3.middleware_stack.add(block_hash_cache_middleware)


def setGasPriceStrategy(gas_price_strategy):
    try:
        blocksToCache = 150
        # adding caching middle ware with LRU Cache and 150 items
        block_hash_cache_middleware = construct_simple_cache_middleware(
        cache_class=partial(LRUCache, blocksToCache),
        rpc_whitelist='eth_getBlockByHash'
        )
        w3.middleware_stack.add(block_hash_cache_middleware)
        # setting the gas Price Strategy
        w3.eth.setGasPriceStrategy(gas_price_strategy)
        print('setted price stratedy')
    except ValueError:
        print('setting Price Strategy was unsuccesful')


class Web3Transaction():
    #Account initalization with priavte Key
    acct = Account.privateKeyToAccount(ETH_PRIVATE_KEY)

    #Cache with 3 categories fast, medium ,slow
    priceCache = Cache(maxsize=3)

    currentNonce = 1235
    #making sure the gas Price can be calculated quickly at any time
    def updateNonce():
        Web3Transaction.currentNonce += 1
        print(Web3Transaction.currentNonce)

    def keepCacheWarm():
        start = timeit.default_timer()

        w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
        Web3Transaction.priceCache.__setitem__('fast',w3.eth.generateGasPrice())

        w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        Web3Transaction.priceCache.__setitem__('medium',w3.eth.generateGasPrice())

        w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
        Web3Transaction.priceCache.__setitem__('slow',w3.eth.generateGasPrice())

        stop = timeit.default_timer()
        print('Time: ', stop - start)
        print(Web3Transaction.priceCache.__getitem__('fast'))
        print(Web3Transaction.priceCache.__getitem__('medium'))
        print(Web3Transaction.priceCache.__getitem__('slow'))
        #print(Web3Transaction.sendTransaction(20,'fast','0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d'))
        Timer(cacheInterval, Web3Transaction.keepCacheWarm).start()


    #takes in the requested eth in wei and returns txHash
    def sendTransaction(gasNeeded, speed, receiver):
        #calculating the gasPrice
        gasPrice = Web3Transaction.priceCache.__getitem__(speed)
        ethNeeded = int(gasPrice * gasNeeded)
        print(is_hex_address(receiver))
        nonce=w3.eth.getTransactionCount(Web3Transaction.acct.address, 'pending')
        #nonce=Web3Transaction.currentNonce
        #Web3Transaction.updateNonce()
        txGasPrice = 20000000000

        transaction = {
            'to': receiver,
            'value': int(ethNeeded),
            'gas': 314150,
            'gasPrice': txGasPrice,
            'nonce': nonce,
            'data': '53656e742066726f6d20676173466175636574202a2e2a',
            'chainId': 3, # Ropsten chain ID
            }
        try:
            signed = Account.signTransaction(transaction, Web3Transaction.acct.privateKey)
            gweiGasPrice = "%.2f" % (gasPrice / 10 ** 9)
            txHash = (w3.eth.sendRawTransaction(signed.rawTransaction)).hex()
            return {"message": "successful",  "txHash":txHash,"gasPrice in Gwei": gweiGasPrice,"Eth sent in Wei":ethNeeded, "link": "https://ropsten.etherscan.io/tx/" + txHash}

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {message}
            #return {"message":"I am not ready yet"}
#print(is_hex_address('160a53c6f8b82f8d5e2b77acfd0aed85116fc512'))
#print(w3.eth.getTransactionCount(Web3Transaction.acct.address, 'pending'))
#Timer(cacheInterval, Web3Transaction.keepCacheWarm).start()

