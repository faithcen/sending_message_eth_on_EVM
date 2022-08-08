from web3 import Web3
from web3.middleware import geth_poa_middleware

if __name__ == "__main__":
    # first run ganache local rpc server with below command
    # $ ganache --fork
    url = "HTTP://127.0.0.1:8545"
    
    # connect RPC server
    w3 = Web3(Web3.HTTPProvider(url))
    if w3.isConnected():
        print("Connected...")

    #### Essential for layers
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3.clientVersion
    
    # get test accounts from ganache
    accounts = w3.eth.accounts
    for acc in accounts:
        print(acc, w3.fromWei(w3.eth.getBalance(acc), 'ether') )
    
    # define tx parameters
    gas = 300000
    to_address = accounts[1] # reciever
    owner = accounts[0] # sender
    txt_message = 'Test message1,\r\n\r\nTest message2,\r\nTest message3' # the message that will be sent 
    
    # construct tx
    construct_txn = {
        'from': owner,
        'to': to_address,
        'nonce': w3.eth.getTransactionCount(owner),
        #'gasPrice': w3.eth.gas_price, #w3.toWei(25, 'gwei') 
        #'gas': gas,
        'data': Web3.toHex(text=txt_message), # text message
        'value': w3.toWei(10, 'ether') # value of ethereum to be sent
        # if just want to send message, you do not need to state value, you could remove it.
        }
    
    # send tx
    tx_hash = w3.eth.send_transaction(construct_txn)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    
    # get tx
    tx_out = w3.eth.getTransaction(tx_hash)
    
    # decode the message that was sent
    print(bytearray.fromhex(tx_out['input'].split('x')[1]).decode())
    
    # check the latest balance of acccounts
    for acc in accounts[:2]:
        print(acc, w3.fromWei(w3.eth.getBalance(acc), 'ether') )
