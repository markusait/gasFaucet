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


class Web3Transaction():
    def __init__(self):
        #Account initalization with priavte Key
        self.acct = Account.privateKeyToAccount(ETH_PRIVATE_KEY)
        #tx object parameters
        self.txGas = 314150
        self.txGasPrice = 20000000000
        self.chainId = 3
        #Cache with 3 categories fast, medium ,slow
        self.priceCache = priceCache = Cache(maxsize=3)
        #web3 instance connecting to node
        self.w3 = Web3(Web3.HTTPProvider(ROPSTEN_URL))
	# caching Parameters
        self.cacheInterval = 30
        self.blocksToCache = 150

        # adding caching middle ware with LRU Cache and 150 items
        block_hash_cache_middleware = construct_simple_cache_middleware(
            cache_class=partial(LRUCache, self.blocksToCache),
            rpc_whitelist='eth_getBlockByHash'
        )
        self.w3.middleware_stack.add(block_hash_cache_middleware)


    def keepCacheWarm(self):

        self.w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
        self.priceCache.__setitem__('fast',self.w3.eth.generateGasPrice())

        self.w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        self.priceCache.__setitem__('medium',self.w3.eth.generateGasPrice())

        self.w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
        self.priceCache.__setitem__('slow',self.w3.eth.generateGasPrice())

        Timer(self.cacheInterval, self.keepCacheWarm).start()


    #takes in the requested gas, speed and tx_receiver returning txHash
    def sendTransaction(self,gasNeeded, speed, receiver):

        #getting the current gasPrice
        gasPrice = self.priceCache.__getitem__(speed)
        #making sure ethNeeded is an int
        ethNeeded = int(gasPrice * gasNeeded)
        #making sure receiver is a eth address todo: implement try, excepet
        print(is_hex_address(receiver))
        nonce=self.w3.eth.getTransactionCount(self.acct.address, 'pending')

        transaction = {
            'to': receiver,
            'value': ethNeeded,
            'gas': self.txGas,
            'gasPrice': self.txGasPrice,
            'nonce': nonce,
            'data': '53656e742066726f6d20676173466175636574202a2e2a',
            'chainId': self.chainId,
            }

        try:
            signed = Account.signTransaction(transaction, self.acct.privateKey)
            gweiGasPrice = "%.2f" % (gasPrice / 10 ** 9)
            txHash = (self.w3.eth.sendRawTransaction(signed.rawTransaction)).hex()
            return {"message": "successful",  "txHash":txHash,"gasPrice in Gwei": gweiGasPrice,"Eth sent in Wei":ethNeeded, "link": "https://ropsten.etherscan.io/tx/" + txHash}

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {message}
