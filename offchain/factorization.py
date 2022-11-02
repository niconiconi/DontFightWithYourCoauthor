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

import sys
import random
def getAuthorList(prod):
    authorListPrime = []
    largestPrime = contract.functions.getlargestPrime().call()
    # get a prime list from 2 to largestPrime
    primeList = []
    visited = [False for i in range(largestPrime + 1)]
    cnt = 0
    for i in range(2, largestPrime + 1):
        if not visited[i]:
            primeList.append(i)
            cnt += 1
        for j in range(cnt):
            if i * primeList[j] > largestPrime:
                break
            visited[i * primeList[j]] = True
            if i % primeList[j] == 0:
                break
    # get the author list
    while prod != 1:
        # get a random index
        index = random.randint(0, len(primeList) - 1)
        # get the prime
        prime = primeList[index]
        if prod % prime == 0:
            authorListPrime.append(prime)
            prod = prod // prime
    authorList = []
    for i in range(len(authorListPrime)):
        authorList.append(contract.functions.getName(authorListPrime[i]).call())
    return authorList

if __name__ == "__main__":
    prod = int(sys.argv[1])
    authors = getAuthorList(prod)
    print(authors)