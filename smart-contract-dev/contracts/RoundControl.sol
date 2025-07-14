// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import "./Registration.sol";

struct Metric {
    uint256 accuracy;
    uint256 f1_score;
    uint256 recall;
    uint256 precision;
    string cid;
    
}
contract Round {
    uint256 public roundId;
    string public globalModelCid;
    // string public nextRoundCid;
    address[] private participants;
    Metric public globalMetrics;
    mapping(address => bool) public isParticipant;
    // mapping(address => string) participantCid;
    mapping(address => Metric) public participantMetrics;

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
            cids[i] = participantMetrics[participants[i]].cid;
        }
        return cids;
    }
    function getGlobalMetrics() public view returns (
        uint256,
        uint256,
        uint256,
        uint256,
        string memory 
        ){
        // Access the struct from the mapping
        Metric storage metrics = globalMetrics;
        // Return the individual fields
        return (
            metrics.accuracy,
            metrics.f1_score,
            metrics.recall,
            metrics.precision,
            metrics.cid
        );
    }

    function getParticipants() public view returns (address[] memory){
        return participants;
    }
    function getParticipantsMetrics(address participantId) public view returns (
        uint256,
        uint256,
        uint256,
        uint256,
        string memory 
        ){
        // Access the struct from the mapping
        Metric storage metrics = participantMetrics[participantId];
        // Return the individual fields
        return (
            metrics.accuracy,
            metrics.f1_score,
            metrics.recall,
            metrics.precision,
            metrics.cid
        );
    }

    function aggregate(
        uint256 accuracy,
        uint256 f1_score,
        uint256 recall,
        uint256 precision,
        string memory _nextRoundCid
        ) public {
        globalMetrics.accuracy = accuracy;
        globalMetrics.f1_score = f1_score;
        globalMetrics.recall = recall;
        globalMetrics.precision = precision;
        globalMetrics.cid = _nextRoundCid;
        // nextRoundCid = _nextRoundCid;
    }

    function submitModelCid(
        address _participant, 
        uint256 _accuracy,
        uint256 _f1_score,
        uint256 _recall,
        uint256 _precision,
        string memory _cid
        ) public {
        require(isParticipant[_participant],"Failed Submit: participant is not registered");
        participantMetrics[_participant] = Metric({
            accuracy:_accuracy,
            f1_score:_f1_score,
            recall:_recall,
            precision:_precision,
            cid:_cid
        });
        // participantCid[participant] = cid;
    }
}

contract RoundControl {
    uint256 public currentRoundId;
    uint256 public numberOfRounds;
    uint64 public noOfParticipants;
    bool public active;
    address public owner;
    string private initialGlobalModelCid;
    Registration private registrationContract;

    mapping(uint256 => address) roundMapping;

    event RoundStarted(uint256 roundId,address roundAddress);
    event RoundEnded(uint256 roundId,address roundAddress);

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
    function setInitialGlobalModleCid(string memory _initialGlobalModelCid) public onlyOwner {
        initialGlobalModelCid = _initialGlobalModelCid;
    }

    function setRoundActive(bool _active) public onlyOwner {
        active = _active;
    }

    function getRound(uint256 _roundId) public view returns (address) {
        return roundMapping[_roundId];
    }

    function createRound(uint64 _noOfParticipants) public onlyOwner returns (address) {
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
            (,,,,string memory cid) = Round(roundMapping[roundId - 1]).globalMetrics();
            Round newRound = new Round(
                currentRoundId,
                cid,
                participants
            );
            roundMapping[currentRoundId] = address(newRound);
        }
        return roundMapping[currentRoundId];
    }

    function nextRound() private {
        currentRoundId = currentRoundId + 1;
        startRound(noOfParticipants);
    }

    function endRound(
        uint256 _accuracy,
        uint256 _f1_score,
        uint256 _recall,
        uint256 _precision,
        string memory _nextRoundCid
        ) public onlyOwner {
        require(active, "Failed end: No active round currently in progress");
        active = false;
        emit RoundEnded(currentRoundId,roundMapping[currentRoundId]);
        Round(roundMapping[currentRoundId]).aggregate(
            _accuracy,
            _f1_score,
            _recall,
            _precision,
            _nextRoundCid
            );
        nextRound();
    }

    function startRound(
        uint64 _noOfParticipants
    ) public onlyOwner returns (address) {
        require(!active, "Failed Start: Round is currently running");
        noOfParticipants = _noOfParticipants;
        address round = createRound(_noOfParticipants);
        active = true;
        emit RoundStarted(currentRoundId,round);
        return round;
    }

    // function submitParticipantCid(string memory cid) public {
    //     require(active, "No active round");
    //     Round(roundMapping[currentRoundId]).submitModelCid(msg.sender, cid);
    // }
}
