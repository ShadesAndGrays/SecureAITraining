# Configuring a Hyperledger Besu network to operate as a gas-free blockchain, 
## Genesis File Configuration
To make your Besu network gas-free,the gensis.json file was modified. This file defines the initial state and rules of your blockchain. Setting the Block Gas Limit to Maximum allows for unlimate computation withing a block as gas cost is no longer a limiting factor for transaction inclusion based on price.

```json
{
  "config": {
    "chainId": 1337,
    // ... other hardforks
    "londonBlock": 0,      // Add this for London hardfork features
    "zeroBaseFee": true,   // For gas-free with London 
    "contractSizeLimit": 2147483647, // Maximum supported size in bytes
    "qbft": {
        // ... QBFT specific configurations
    }
  },
  "gasLimit": "0x1fffffffffffff", // Set to maximum
  // ... other genesis fields
}
```


Setting `min-gas-price` to `0` during startup or in the `config.toml`  for Besu nodes to accept transactions with a gasPrice of zero. Any node with a non-zero min-gas-price will silently drop such transactions. 

## Config.toml 

```toml
# ...
min-gas-price=0
```

## Startup 

To start up the besu network run the following command

```bash
docker compose up
```
To run as  a background process 
```bash
docker compose up --detach
```
 or
```bash
docker-compose up -d
```
