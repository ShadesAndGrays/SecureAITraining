# Initial Validators

This directory contains instructions for generating the `extraData` field for QBFT consensus in Hyperledger Besu.

## Steps

1. Create a file named `toEncode.json` in the `data` directory.
2. The file should contain an array of validator node addresses (4 are required).
3. Encode the data using Besu:

   **If Besu is installed locally:**
   ```sh
   besu rlp encode --from=/data/toEncode.json --type=QBFT_EXTRA_DATA
   ```

   **Or using Docker:**
   ```sh
   docker run --rm -v "$PWD/data:/data" hyperledger/besu:latest rlp encode --from=/data/toEncode.json --type=QBFT_EXTRA_DATA
   ```

4. Copy the output and add it to your `genesis.json` as the `extraData` attribute.