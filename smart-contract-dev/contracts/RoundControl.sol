// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

import "./Registration.sol";

contract Round {
    uint256 public roundId;
    string public globalModelCid;
    string public nextRoundCid;
    address[] private participants;
    mapping(address => bool) public isParticipant;
    mapping(address => string) participantCid;

    constructor(
        uint256 _roundId,
        string memory _globalModelCid,
        address[] memory _participants

    ) {
        roundId = _roundId;
        globalModelCid = _globalModelCid;
        participants = _participants;
        for (uint i = 0; i < participants.length; i++){
            isParticipant[participants[i]] = true;
        }
    }

    function isRegistered(address participant) public view returns (bool) {
        return isParticipant[participant];
    }

    function getCids() public view returns (string[] memory) {
        string[] memory cids = new string[](participants.length);
        for (uint i = 0; i < participants.length; i++) {
            cids[i] = participantCid[participants[i]];
        }
        return cids;
    }
    function getParticipants() public view returns (address[] memory){
        return participants;
    }

    function Aggregate(string memory _nextRoundCid) public {
        nextRoundCid = _nextRoundCid;
    }

    function submitModelCid(address participant, string memory cid) public {
        require(isParticipant[participant],"Failed Submit: participant is not registered");
        participantCid[participant] = cid;
    }
}

contract RoundControl {
    uint256 public currentRoundId;
    bool public active;
    address public owner;
    string private initialGlobalModelCid;
    Registration private registrationContract;

    mapping(uint256 => address) roundMapping;

    event RoundStarted(uint256 roundId);
    event RoundEnded(uint256 roundId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    constructor(string memory _initialGlobalModelCid,address _registrationContract) {
        active = false;
        currentRoundId = 0;
        owner = msg.sender;
        initialGlobalModelCid = _initialGlobalModelCid;
        registrationContract = Registration(_registrationContract);
    }

    function setRoundActive(bool _active) public onlyOwner {
        active = _active;
    }

    function getRound(uint256 _roundId) public view returns (address) {
        return roundMapping[_roundId];
    }

    function createRound(uint64 _noOfParticipants) public onlyOwner returns (uint256) {
        require(!active, "Failed Create: Round is Currently active");

        uint256 roundId = currentRoundId;
        address[] memory participants = registrationContract.getRandomRegistrant(_noOfParticipants);  // Get random of registrants

        if (roundId == 0) {
            // First Round
            Round newRound = new Round(
                currentRoundId,
                initialGlobalModelCid,
                participants
            );
            roundMapping[currentRoundId] = address(newRound);
        } else {
            Round newRound = new Round(
                currentRoundId,
                Round(roundMapping[roundId - 1]).nextRoundCid(),
                participants
            );
            roundMapping[currentRoundId] = address(newRound);
        }
        return roundId;
    }

    function nextRound() private {
        currentRoundId = currentRoundId + 1;
    }

    function endRound() public onlyOwner {
        require(active, "Failed end: No active round currently in progress");
        active = false;
        emit RoundEnded(currentRoundId);
        nextRound();
    }

    function startRound(
        uint64 _noOfParticipants
    ) public onlyOwner returns (uint256) {
        require(!active, "Failed Start: Round is currently running");
        createRound(_noOfParticipants);
        active = true;
        emit RoundStarted(currentRoundId);
        return currentRoundId;
    }

    function submitParticipantCid(string memory cid) public {
        require(active, "No active round");
        Round(roundMapping[currentRoundId]).submitModelCid(msg.sender, cid);
    }
}
