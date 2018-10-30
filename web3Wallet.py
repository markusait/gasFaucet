from web3 import Web3, HTTPProvider
from eth_account import Account
import os

token = os.environ['INFURA_TOKEN']
url = "https://ropsten.infura.io/%s" % token
w3 = Web3(Web3.HTTPProvider(url))


def sendTransaction(ethNeeded):
    transaction = {
        'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
        'value': ethNeeded,
        'gas': 2000000,
        'gasPrice': 4321,
        'nonce': 400000000,
        'chainId': 3, # Ropsten chain ID
        }
    key = os.environ['ETH_PRIV_KEY']
    signed = Account.signTransaction(transaction, key)
    return w3.eth.sendRawTransaction(signed.rawTransaction)
