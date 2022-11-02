// SPDX-License-Identifier: GPL-3.0
pragma solidity >= 0.5.0;
// prime map
contract Storage {
    uint256 largestPrime;
    mapping(uint256 => string) nameDBinv;
    mapping(string => uint256) nameDB;
    //initialize to largestPrime to 1
    constructor() public {
        largestPrime = 2;
    }
    function getlargestPrime() public view returns (uint) {
        return largestPrime;
    }
    function setlargestPrime(uint256 _largestPrime, string memory name) public {
        require(largestPrime < _largestPrime, "largestPrime must be larger than current largestPrime");
        // check if _largestPrime is not too large 
        // prime gap is less than 1000 for practical purposes
        require(_largestPrime - largestPrime < 1000, "prime gap is too large");
        // check if name already exists
        require(nameDB[name] == 0, "name already exists");
        nameDB[name] = _largestPrime;
        nameDBinv[_largestPrime] = name;
        largestPrime = _largestPrime;
    }
    function getName(uint256 _largestPrime) public view returns (string memory) {
        return nameDBinv[_largestPrime];
    }
    function getPrime(string memory name) public view returns (uint256) {
        return nameDB[name];
    }
}