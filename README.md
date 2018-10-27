# gasFaucet API
---
Calculating how much Ether should be sent to a wallet depending on requested gas price, gas amount and confirmation time.


__Usage__

install flask

`pip3 install flask`

run the app

`python3 app.py`

send request to localhost with query parameters

example GET request:

`http://localhost:8000/fill-wallet-for-gas?gas_needed=10000&tx_speed=medium&public_address=0x516F329EC1fF7BF6882dE762A14eb94491FA4D8d`
