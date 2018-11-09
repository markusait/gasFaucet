from config import ETH_PRIVATE_KEY, NODE_URL, CACHE_INTERVAL
from web3 import Web3, HTTPProvider, middleware
from web3.auto import w3
from web3.gas_strategies.time_based import fast_gas_price_strategy, slow_gas_price_strategy,medium_gas_price_strategy
from web3.middleware.cache import construct_simple_cache_middleware
from eth_account import Account
from cachetools import LRUCache, Cache
from functools import partial
from threading import Timer
import json
import requests

class Web3Transaction():
    def __init__(self):
        #Web3 instance connecting to node
        self.w3 = Web3(Web3.HTTPProvider(NODE_URL))
        
	#Cache with 3 categories fast, medium ,slow
        self.priceCache = priceCache = Cache(maxsize=3)
        
	#Caching Parameters
        self.cacheInterval = CACHE_INTERVAL
        self.blocksToCache = 150
        
	# Construct Cache with  with LRU Cache and 150 items
        self.block_hash_cache_middleware = construct_simple_cache_middleware(
            cache_class=partial(LRUCache, self.blocksToCache),
            rpc_whitelist='eth_getBlockByHash'
        )
    	#Adding caching to middle ware
        self.w3.middleware_stack.add(self.block_hash_cache_middleware)

        #Faucet Account initalization with priavte Key
        self.faucetAccount = Account.privateKeyToAccount(ETH_PRIVATE_KEY)
	
	#Transaction parameters of faucet
        self.txGas = 314150
        self.txGasPrice = 20000000000
        self.chainId = 3
        self.txData = '53656e742066726f6d20676173466175636574202a2e2a'
	

    #getting the current nonce from connected parity node with parity nextNonce method over http
    def getNonce(self):
        try:
            headers = {'Content-type': 'application/json'}
            url = NODE_URL
            data = {"method":"parity_nextNonce","params":[self.faucetAccount.address],"id":1,"jsonrpc":"2.0"}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            #hex number is returned
            hexNum = r.json()['result']
            return int(hexNum, 0)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {message}

    #Connection checking
    def checkConnection(self):
        print(self.w3)
        try:
            version = self.w3.version.node
        except:
            print('error, not connected')

    #Keeping middle ware cache warm and update prices quickly
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
        #gasPrice = self.priceCache.__getitem__(speed)
        gasPrice = 10
	#calculating the gas needed Ether as int
        ethNeeded = int(gasPrice * gasNeeded)
        
        #geting the current nonce 
        #nonce = self.getNonce()
        nonce = 0
        transaction = {
            'to': receiver,
            'value': ethNeeded,
            'gas': self.txGas,
            'gasPrice': self.txGasPrice,
            'nonce': nonce,
            'data': self.txData,
            'chainId': self.chainId
            }

        try:
            signed = Account.signTransaction(transaction, self.faucetAccount.privateKey)
            gweiGasPrice = "%.2f" % (gasPrice / 10 ** 9)
            txHash = (self.w3.eth.sendRawTransaction(signed.rawTransaction)).hex()
            return {"message": "successful",  "txHash":txHash,"gasPrice in Gwei": gweiGasPrice,"Eth sent in Wei":ethNeeded, "link": "https://ropsten.etherscan.io/tx/" + txHash}

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            #checking for insufficient funds
            if(ex.args[0]['message'].split()[0] == 'insufficient'):
                print('yaay')
            return {message}



newTx  = Web3Transaction()
#newTx.keepCacheWarm()
print(newTx.sendTransaction(10,'fast','0x2621ea417659Ad69bAE66af05ebE5788E533E5e7'))
