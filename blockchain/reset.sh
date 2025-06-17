#!/bin/bash
cd data || exit 1
for D in besu*/; do
    echo "Processing $D"
    cd "$D" || continue
    # Delete all files except 'key'
    find . -maxdepth 1 -type f ! -name 'key' -exec rm -f {} +
    # Delete all directories except 'key'
    find . -maxdepth 1 -type d ! -name '.' ! -name 'key' -exec rm -rf {} +
    cd ..
done
echo "Done!"
read -p "Press enter to continue"
