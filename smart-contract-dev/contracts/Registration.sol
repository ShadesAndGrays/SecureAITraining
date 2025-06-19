// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract Registration {

  address[] private registrants;
  mapping (address => bool) private registration_list;
  mapping (address => bool) private banned_list;
  address private owner;

  constructor(){
    owner = msg.sender;
  }

  /// @notice Returns random registrants
  /// @param count number of registants to be returned
  function getRandomRegistrant(uint count) public view returns (address[] memory){
    require(count <= registrants.length);
    require(count < 256); // max block stored
    address [] memory pool = registrants;
    address[] memory selected = new address[](count);
    uint n = pool.length;

    for (uint i = 0; i < count; i++){
      // Pseudo-radom
      uint rand = uint(keccak256(abi.encodePacked(blockhash(block.number - i),block.timestamp,i))) % n;
      selected[i] = pool[rand];
      // To avoid duplicates
      pool[rand] = pool[n-1]; // replace chosen with last
      n--;
    }
    return selected;
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
    registrants.push(client);
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