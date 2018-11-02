from web3 import Web3, HTTPProvider
from eth_account import Account
import os

#connection to node
w3 = Web3(Web3.HTTPProvider(os.environ['INFURA_URL']))

#Account initalization with priavte Key
acct = Account.privateKeyToAccount(os.environ['ETH_PRIV_KEY'])
print('maKING TX NOW')
#takes in the requested eth in wei and returns txHash
def sendTransaction(ethNeeded):
    #TODO: increment manually after each call
    nonce=w3.eth.getTransactionCount(acct.address, 'latest')
    transaction = {
        'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
        'value': ethNeeded,
        'gas': 2000000,
        'gasPrice': 1,
        'nonce': nonce,
        'data': '53656e742066726f6d20676173466175636574202a2e2a',
        'chainId': 3, # Ropsten chain ID
        }
    signed = Account.signTransaction(transaction, acct.privateKey)
    txHash = w3.eth.sendRawTransaction(signed.rawTransaction)
    print(txHash)
    return txHash.hex()

#print(sendTransaction(99999))




