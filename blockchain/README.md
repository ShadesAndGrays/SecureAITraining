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