seckey = "04737ad0e62c6340bdbf3e1982e6b5cc8b9d5e9f399727f89e25014b565dcd68"
pubkey = "0x0AaF355bc2555A1C1f0E5C4554FB9E9F9AcEcBc0"

contractAddress = "0xc3330141237A773BAAc6818b4c00a5490f853Fc6"
infura_url = "https://goerli.infura.io/v3/484c97d55d964cf58e0021dc53bde5cd"

import json
import web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
w3 = Web3(Web3.HTTPProvider(infura_url))
# goerli testnet
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# get abi string from ../artifacts/contracts/storage.sol/Storage.json
f = open("../contracts/abi/Storage.abi", "r")
abi = json.loads(f.read())

contract = w3.eth.contract(address=contractAddress, abi=abi)
# set gas price strategy
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

def Register(name):
    # get the latest prime
    latestPrime = contract.functions.getlargestPrime().call()
    print("Latest prime: ", latestPrime)

    def isPrime(x):
        if x <= 1:
            return False
        elif x <= 3:
            return True
        elif x % 2 == 0 or x % 3 == 0:
            return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i = i + 6
        return True

    # get the next prime
    for i in range(latestPrime + 1, latestPrime + 1000):
        if isPrime(i):
            nextPrime = i
            print("Next prime: ", nextPrime)
            break

    # set the next prime
    nonce = w3.eth.getTransactionCount(pubkey)
    gasPrice = int(w3.eth.generate_gas_price() * 1.4)
    print('gasPrice:', gasPrice)
    tx = contract.functions.setlargestPrime(nextPrime, name).buildTransaction({
        'chainId': 5,
        'gas': 100000,
        'gasPrice': gasPrice,
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.signTransaction(tx, private_key=seckey)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print("Transaction hash: ", tx_hash.hex())

    # wait for the transaction to be mined
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Transaction receipt: ", tx_receipt)
    return nextPrime

def getPrimeByName(name):
    prime = contract.functions.getPrime(name).call()
    print(prime)
    return prime
def getNameByPrime(x):
    name = contract.functions.getName(x).call()
    print(name)
    return name

import sys

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "register":
        name = sys.argv[2]
        Register(name)
    elif mode == "getPrime":
        name = sys.argv[2]
        getPrimeByName(name)
    elif mode == "getName":
        x = int(sys.argv[2])
        getNameByPrime(x)
    elif mode == "aggerate":
        names = sys.argv[2:]
        prod = 1
        for name in names:
            p = getPrimeByName(name)
            prod *= p
        print("Aggerate result: ", prod)