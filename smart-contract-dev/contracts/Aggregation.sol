// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract Aggregation {
  int256 public constant DECIMALS = 1e18;

  int private roundId; // The current round being carried out

  int256[][] private model_updates; // Nested arrays for handling complex types like neural netwroks

  address private owner;

  constructor(int _roundId){
    owner = msg.sender;
    roundId = _roundId;
  }

  function getRound() public view returns (int) {
    return roundId;
  }

  // function addModelUpdate(int256[][] update) public view  calldata returns (int) {
  //   return roundId;
  // }

}