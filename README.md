# gasFaucet API

---
Calculating how much Ether should be sent to a wallet depending on requested gas price, gas amount and confirmation time.


__Installation__

install dependences

`pip3 install -r requirements.txt`

populate the config.py with:

- ROPSTEN_URL = "https://ropsten.infura.io/YOUR_API_KEY"
- MAINNET_URL = "https://mainnet.infura.io/YOUR_API_KEY"
- ETH_PRIVATE_KEY = Ethereum Private Key as string
- API_KEY = Random 30 characters long string  
- CACHE_INTERVAL = Positive integer for seconds
__Usage__

run the app

`python3 app.py`

send request to localhost with query parameters

available parameters are:
`gas_needed` (1 - 4.000.000)
`tx_speed` (slow, medium, fast)
`public_address` (valid ethereum address)

example GET request:

`curl  http://localhost:8000/fill-wallet-for-gas?gas_needed=10000&tx_speed=medium&public_address=0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d'`
