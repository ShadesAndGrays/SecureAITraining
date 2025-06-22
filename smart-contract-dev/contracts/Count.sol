// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract Count {
    uint32 public count;

    event countChanged(uint32 count);

    constructor(uint32 _count) {
        require(
            0 < _count,
            "Count should not be negative"
        );
        count = _count;
    }

    function increment() public {
        count += 1;
        emit countChanged(count);
    }
}