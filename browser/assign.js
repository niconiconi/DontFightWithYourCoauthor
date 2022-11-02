const Web3 = require('web3');
const web3 = new Web3('ws://localhost:8546');
console.log(web3);
const rpcURL = "https://goerli.infura.io/v3/484c97d55d964cf58e0021dc53bde5cd"

//invoke the metamask
if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');
}

const ethereumButton = document.querySelector('.enableEthereumButton');

ethereum.request({ method: 'eth_requestAccounts' });
const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
const account = accounts[0];