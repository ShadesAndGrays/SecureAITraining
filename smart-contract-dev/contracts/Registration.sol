// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract Registration {

  mapping (address => bool) private registration_list;
  mapping (address => bool) private banned_list;
  address private owner;

  constructor(){
    owner = msg.sender;
  }

  function getOwner() public view returns (address){
    return owner;
  }
  function isValid(address client) public view returns (bool) {
    return registration_list[client] && !banned_list[client];

  }

  function isRegistered(address client) public view returns (bool) {
    return registration_list[client];
  }

  function isBanned(address client) public view returns (bool) {
    return banned_list[client];
  }

  function register(address client) public {
    require(!registration_list[client],"Client cannot register twice");
    registration_list[client] = true;
  }

  function unregister(address client) public {
    require(registration_list[client],"Client must not be registered");
    registration_list[client] = false;
  }

  function ban(address client) public {
    require(registration_list[client],"Client must be registered");
    banned_list[client] = true;
  }

}