from web3 import Web3
from web3.middleware import geth_poa_middleware

if __name__ == "__main__":
    # first run ganache local rpc server
    # $ ganache --fork
    url = "HTTP://127.0.0.1:8545"

    w3 = Web3(Web3.HTTPProvider(url))
    if w3.isConnected():
        print("Connected...")

    #### Essential for Avalanche
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3.clientVersion
    accounts = w3.eth.accounts
    for acc in accounts:
        print(acc, w3.fromWei(w3.eth.getBalance(acc), 'ether') )
    
    gas = 300000
    to_address = accounts[1]
    owner = accounts[0] #, to_address, 0.1, acct
    txt_message = 'Test message1,\r\n\r\nTest message2,\r\nTest message3 '
    construct_txn = {
        'from': owner,
        'to': to_address,
        'nonce': w3.eth.getTransactionCount(owner),
        #'gasPrice': w3.eth.gas_price, #w3.toWei(25, 'gwei') 
        #'gas': gas,
        'data': Web3.toHex(text=txt_message),
        'value': w3.toWei(10, 'ether')

        }
    
    tx_hash = w3.eth.send_transaction(construct_txn)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_out = w3.eth.getTransaction(tx_hash)
    print(bytearray.fromhex(tx_out['input'].split('x')[1]).decode())

    for acc in accounts[:2]:
        print(acc, w3.fromWei(w3.eth.getBalance(acc), 'ether') )
