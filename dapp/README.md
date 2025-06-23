# DAPP

This is the front end of the application. Users will be able to interact with the smart contract deployed on the blockchain.  
For the prototype, a single flask server would be used to simulate multiple clients performing the training

The users would be able to:  
- [x] Connect the wallet
- [x] Register to participate in the federated learning process
- [ ] 



## Usage

A React + TypeScript + Vite template was used which provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

There are two stages to running the application.

In the root directory of the sub project, Start the dapp 

```bash
npm run dev

```
This should start up the dapp on port [5173](http://localhost:5173)

Secondly, run the python application on port 

```bash
cd scripts
flask --app flasker run --debug
```
This should start up the python on port **5000**
