import Web3 from "web3";

import RegistrationArtifact from "./Contracts/Registration.json";
import CountArtifact from "./Contracts/Count.json";

const warning = document.getElementById("warn")
const accountDiv = document.getElementById("account")

// Event Listeners
document.getElementById('connectWalletBtn').addEventListener('click', requestAccounts);

const registration_contract_address = import.meta.env.VITE_REGISTER_CONTRACT_ADDRESS;

let contracts = {}
let allAccounts = []
let web3 = {}


function setWarning(msg){
  warning.innerText = msg;
}

function setAccount(account){
    accountDiv.innerText = account;
}


// ensure that there is an injected the Ethereum provider
if (window.ethereum) {
  // use the injected Ethereum provider to initialize Web3.js
  web3  = new Web3(window.ethereum);
  setWarning("Web3 Initialized");
} else {
  // no Ethereum provider - instruct user to install MetaMask
  setWarning("Please install MetaMask");
}



if (web3) {
  let c = new web3.eth.Contract( RegistrationArtifact.abi, registration_contract_address);
  c.handleRevert = true;
  contracts["Registration"] = c;
  c = new web3.eth.Contract(CountArtifact.abi, "");


const subscription = c.events.countChanged();
  subscription.on('data', (event) => {
              console.log('ValueUpdated event received:', event);
              console.log('Value:', event.returnValues.count);
              const val = Number(event.returnValues.count);
              setValue(val);
          })
}else{
  console.error("Web3 is not initialized. Cannot use Contracts")
}

// Example function of interacting with local python flask server
let getFactorial = () => {
  fetch(`/api/calculate?number=${input}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      setCount(Number(data.result));
    })
    .catch((error) => console.error("Error:", error));
};

async function requestAccounts(){
  if (web3 === null) {
    console.log("Web3 is not initialzed");
    return;
  }

  await window.ethereum.request({ method: "eth_requestAccounts" });
  allAccounts = await web3.eth.getAccounts();

  setAccount(allAccounts[0]);
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
    setWarning("Transaction failed: " + error.message);
  }
};

// Navigation/page switching logic
export function showPage(pageId) {
  document.getElementById('proposerPage').style.display = 'none';
  document.getElementById('participantPage').style.display = 'none';
  document.getElementById('dashboardPage').style.display = 'none';
  document.getElementById(pageId).style.display = 'block';
}

// Show proposer page by default on load
showPage('proposerPage');

// Federated learning type selection for proposer
export function startFL(type) {
  document.getElementById('proposerStatus').innerText = `Started federated learning: ${type}`;
  // TODO: Call backend to start FL with selected type
}

function showWarn(msg) {
  const warn = document.getElementById('warn');
  warn.innerText = msg;
  warn.classList.add('active');
  setTimeout(() => warn.classList.remove('active'), 3000);
}
// Attach navigation to nav buttons
window.showPage = showPage;
window.startFL = startFL;