All smart contracts are located in the `contracts` folder.

## Starting a Hardhat Server

```bash
npx hardhat node --hostname 127.0.0.1 --port 8545
```

alternately run `npm run launch:dev`

http://127.0.0.1:8545 is the default, so the following is also equivalent:

```bash
npx hardhat node
```

Scripts for interaction and end-to-end testing are found in the `./scripts` folder.

Currently, Ignition is used to deploy the smart contracts:

```bash
npx hardhat ignition deploy .\ignition\modules\{*}.ts --network localhost
```

additionally, Ignition

