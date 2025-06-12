import { useEffect, useState } from "react";
import { Web3, Contract } from "web3";

import "./App.css";
import RegistrationArtifact from "./Contracts/Registration.json";

function App() {
  const [input, setInput] = useState(1);
  const [count, setCount] = useState(1);
  const [warning, setWarning] = useState<string | null>(null);
  const [web3, setWeb3] = useState<Web3 | null>(null);
  const [connectButtonDisabled, setConnectButtonDisabled] =
    useState<boolean>(false);
  const [accounts, setAccounts] = useState<string[] | null>(null);
  const [connectedAccount, setConnectedAccount] = useState<string | null>(null);
  const [contract, setContract] = useState<Contract<any> | null>(null);

  contract;
  setContract;
  // Set up web3
  useEffect(() => {
    // ensure that there is an injected the Ethereum provider
    if (window.ethereum) {
      // use the injected Ethereum provider to initialize Web3.js
      setWeb3(new Web3(window.ethereum));
      setConnectButtonDisabled(false);
    } else {
      // no Ethereum provider - instruct user to install MetaMask
      setWarning("Please install MetaMask");
      setConnectButtonDisabled(true);
    }
  }, []);

  useEffect(() => {
    const deployed_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3";
    const abi = RegistrationArtifact.abi;
    console.log(abi);
    if (web3) {
      const c = new web3.eth.Contract(abi, deployed_address);
      c.handleRevert = true;
      setContract(c);
    }
  }, [web3]);

  // Example function of interacting with local python flask server
  let getFactorial = () => {
    fetch(`http://localhost:5000/calculate?number=${input}`)
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setCount(Number(data.result));
      })
      .catch((error) => console.error("Error:", error));
  };
  let requestAccounts = async () => {
    if (web3 === null) {
      console.log("Web3 is not initialzed");
      return;
    }

    await window.ethereum.request({ method: "eth_requestAccounts" });
    const allAccounts = await web3.eth.getAccounts();

    setAccounts(allAccounts);
    setConnectedAccount(allAccounts[0]);
    console.log(
      "Web3 is initialized Account: ",
      allAccounts[0],
      allAccounts?.length
    );
  };

  const handleRegister = async () => {
    if (!contract || !connectedAccount) {
      setWarning("Contract / Account is not initialized");
      return;
    }
    try {
      const tx = await contract.methods
        .register(connectedAccount)
        .send({ from: connectedAccount });

      console.log("Transaction successful:", tx);
      setWarning("Registration successful!");
    } catch (error) {
      console.error("Transaction failed", error);
      setWarning("Transaction failed: " + (error as Error).message);
    }
  };
  return (
    <>
      <div>
        <div id="account">
          {connectedAccount ? `Address:  ${connectedAccount}` : ""}
        </div>
        <h1> Federated Day </h1>
        <div id="warn" style={{ color: "red" }}>
          {warning}
        </div>
        <p>
          Register to participate in the Blockchain Federated Learning Process
        </p>
        <button
          onClick={() => requestAccounts()}
          disabled={connectButtonDisabled}
        >
          {" "}
          Connect Wallet
        </button>
        <button
          onClick={handleRegister}
          disabled={!connectedAccount || !contract}
        >
          Register on Blockchain
        </button>
      </div>
    </>
  );
}

export default App;
