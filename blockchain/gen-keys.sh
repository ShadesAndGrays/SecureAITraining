#!/bin/bash

read -p "Enter number of keys pairs to create: " num

echo "This will take some time..."
echo "Creating temp data dir"
mkdir data -p

while [[ $num -gt 0 ]]; do

echo "Creating random private key $num" 
num=$((num-1))
# Generate a private key
openssl rand -hex 32 | sed 's/^/0x/' > key

# move key to data directory
mv key data/

echo "Extracting public key"
# Extract the public key
docker run --rm -v./data/:/opt/besu/data/ hyperledger/besu  public-key  export --node-private-key-file=/opt/besu/data/key --to=/opt/besu/data/key.pub > /dev/null 

echo "Creating key folder"
# Generate the node address using Besu
node_addr=$(docker run --rm -v ./data/:/opt/besu/data/ hyperledger/besu public-key export-address --node-private-key-file=/opt/besu/data/key | tail -n 1)

# make node address folder
mkdir -p keys/$node_addr

# move contents of data to node_address folder
mv data/* keys/$node_addr

done
# clean up data dir
rm data -r

echo "Done"
