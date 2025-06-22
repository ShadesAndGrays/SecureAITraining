# Blockchain

This directory contains a Docker Compose YAML file for starting a Hyperledger Besu Proof-of-Authority blockchain with 4 validators.

## Scripts

- The `keys` folder contains a set of test keys for convenience. **Do not use these keys in a production environment.**
- The `gen-keys.sh` script uses Besu's public-key component and OpenSSL to generate keys. It creates a `keys` folder (remove it after use or add it to `.gitignore`).
- The `reset.sh` script removes all content from the generated data directories except the root folders and keys.

## Usage

Start the network:
```sh
docker compose up
```
Or run in detached mode:
```sh
docker compose up -d
```

## Configuration

- Common configuration is stored in `config/besu/config.toml`.
- Node-specific settings are hardcoded in `docker-compose.yaml`.
- The genesis block is defined in `config/besu/genesis.json`.


## Free Gas Netwrok
The network is currently configures to use qbft concensus mechanism. A **POA** concensus mechanism

To configure a qbft network, make the following changes to the config section of the `config/besu/gensis.json` file
```json
{
  "config": {
    ...
      "qbft": {
          "epochlength": 30000,
          "blockperiodseconds": 5,
          "requesttimeoutseconds": 10
      }
  }
}
```
Futhermore we create a gas free network for the prototype using the following set of changes
```json
{
  "config": {
    ...
    "contractSizeLimit": 2147483647,
    ...
  }
  ...
  "gasLimit": "0x1fffffffffffff",
}
```

and the following entry in the config file
```toml
min-gas-price=0
```