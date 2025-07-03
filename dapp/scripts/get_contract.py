#!/bin/python

import os
import shutil
import json
import re

# Directories
root = '/home/shadowuser/Dev/FinalYearProject/SecureAITraining/'
sub_directory = 'dapp/Contracts/'
contract_directory = "smart-contract-dev/artifacts/contracts"
env_path = 'dapp/.env'

mapping = {
    'Count.sol/Count.json': 'Count.json',
    'Registration.sol/Registration.json': 'Registration.json',
    'RoundControl.sol/RoundControl.json': 'RoundControl.json',
    'RoundControl.sol/Round.json': 'Round.json'
}

src_dir = os.path.join(root, contract_directory)
dst_dir = os.path.join(root, sub_directory)

# Ensure destination directory exists
os.makedirs(dst_dir, exist_ok=True)

for src_name, dst_name in mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_path} to {dst_path}")
    else:
        print(f"File not found: {src_path}")

deployed_address_file = "/home/shadowuser/SecureAITraining/smart-contract-dev/ignition/deployments/chain-31337/deployed_addresses.json"
deployed_address_module = [
   'FeduntuModule#Registration',
   'FeduntuModule#RoundControl',
   'FeduntuModule#Count']

def pascal_to_scream(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.upper()

j = json.load(open(deployed_address_file))

# updating env


with open(os.path.join(root, env_path),'w') as f:
  text = "# PORT\n"
  text += 'VITE_PYTHON_SERVER_PORT=5000\n\n' 
  text += '# CONTRACTS DEPLOYED\n' 
  for i in deployed_address_module:
    text += f'VITE_{pascal_to_scream(i.split('#')[1])}_CONTRACT_ADDRESS={j[i]}\n'
  f.write(text)

