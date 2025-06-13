// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

contract Aggregation {
    int256 public constant DECIMALS = 1e18;
    int256 private roundId; // The current round being carried out
    address private owner;

    // Store encrypted model updates as bytes arrays (Paillier ciphertexts)
    bytes[] private encryptedUpdates;
    bool public aggregationComplete;
    bytes public aggregatedEncryptedModel; // The aggregated encrypted model (Paillier sum)
    string public aggregatedModelCid; // IPFS CID of the decrypted aggregated model

    event EncryptedUpdateSubmitted(address indexed participant, uint256 updateIndex);
    event AggregationCompleted(bytes aggregatedEncryptedModel);
    event AggregatedModelCidStored(string cid);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not contract owner");
        _;
    }

    constructor(int256 _roundId) {
        owner = msg.sender;
        roundId = _roundId;
        aggregationComplete = false;
    }

    /// @notice Submit an encrypted model update (Paillier ciphertext)
    /// @param encryptedUpdate The encrypted model update as bytes
    function submitEncryptedUpdate(bytes calldata encryptedUpdate) external {
        require(!aggregationComplete, "Aggregation already completed");
        encryptedUpdates.push(encryptedUpdate);
        emit EncryptedUpdateSubmitted(msg.sender, encryptedUpdates.length - 1);
    }

    /// @notice Aggregate encrypted updates (off-chain aggregation recommended for gas efficiency)
    /// @param _aggregatedEncryptedModel The aggregated encrypted model (Paillier sum) as bytes
    function completeAggregation(bytes calldata _aggregatedEncryptedModel) external onlyOwner {
        require(!aggregationComplete, "Aggregation already completed");
        aggregatedEncryptedModel = _aggregatedEncryptedModel;
        aggregationComplete = true;
        emit AggregationCompleted(_aggregatedEncryptedModel);
    }

    /// @notice Store the IPFS CID of the decrypted aggregated model
    /// @param cid The IPFS CID string
    function storeAggregatedModelCid(string calldata cid) external onlyOwner {
        require(aggregationComplete, "Aggregation not complete");
        aggregatedModelCid = cid;
        emit AggregatedModelCidStored(cid);
    }

    /// @notice Get the number of encrypted updates submitted
    function getEncryptedUpdateCount() external view returns (uint256) {
        return encryptedUpdates.length;
    }

    /// @notice Get a specific encrypted update by index
    function getEncryptedUpdate(uint256 index) external view returns (bytes memory) {
        require(index < encryptedUpdates.length, "Index out of bounds");
        return encryptedUpdates[index];
    }

    /// @notice Get the round ID
    function getRound() public view returns (int256) {
        return roundId;
    }
}