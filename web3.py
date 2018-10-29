from web3 import Web3, HTTPProvider
from eth_account import Account
import os

token = os.environ['INFURA_TOKEN']
url = "https://ropsten.infura.io/%s" % token
w3 = Web3(Web3.HTTPProvider(url))
