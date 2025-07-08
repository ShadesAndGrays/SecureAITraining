import Web3, { Contract } from "web3";

import CountArtifact from "./Contracts/Count.json";
import RegistrationArtifact from "./Contracts/Registration.json";
import RoundArtificat from "./Contracts/Round.json";
import RoundControlArtificat from "./Contracts/RoundControl.json";
// import { PinataSDK } from "pinata";

const count_contract_address = import.meta.env.VITE_COUNT_CONTRACT_ADDRESS;
const round_control_contract_address = import.meta.env
  .VITE_ROUND_CONTROL_CONTRACT_ADDRESS;
const registration_contract_address = import.meta.env
  .VITE_REGISTRATION_CONTRACT_ADDRESS;

// const pinata_jwt = import.meta.env.VITE_PINATA_JWT
// const pinata_gateway = import.meta.env.VITE_PINATA_GATEWAY
// const pinata = new PinataSDK({
//   pinataJwt: pinata_jwt,
//   pinataGateway: pinata_gateway,
// });
const warning = document.getElementById("warn");

// Event Listeners
document
  .getElementById("connectWalletBtn")
  .addEventListener("click", requestAccounts);

document
  .getElementById("disconnectWalletBtn")
  .addEventListener("click", disconnectAccount);
document
  .getElementById("registerBtn")
  .addEventListener("click", handleRegister);

document
  .getElementById("flConfigForm")
  .addEventListener("submit", proposeTraining);

document
  .getElementById("deactivateRoundBtn")
  .addEventListener("click", deactivateRound);

let contracts = {};
let connectedAccount;
let currentRoundId;
let web3 = {};

function setWarning(msg, positive = false) {
  if (msg.length == 0) {
    warn.classList.remove("show");
  }
  if (positive) {
    warn.classList.add("positive");
  } else {
    warn.classList.remove("positive");
  }

  warning.innerText = msg;
  warn.classList.add("show");
  setTimeout(() => warn.classList.remove("show"), 3000);
}
function toggleAccountAddress(on = true) {
  let accountAddress = document.getElementById("accountAddress");
  if (on) {
    accountAddress.classList.add("show");

    document.getElementById("connectWalletBtn").disabled = true;
    document.getElementById("disconnectWalletBtn").classList.add("show");
  } else {
    accountAddress.classList.remove("show");
    document.getElementById("connectWalletBtn").disabled = false;
    document.getElementById("disconnectWalletBtn").classList.remove("show");
  }
}

// ensure that there is an injected the Ethereum provider
if (window.ethereum) {
  // use the injected Ethereum provider to initialize Web3.js
  // web3 = new Web3(window.ethereum);
  web3 = new Web3("http://127.0.0.1:8545");
  setWarning("Metamask Initialized", true);
} else {
  // no Ethereum provider - instruct user to install MetaMask
  setWarning("Please install MetaMask");
}

// Connect to web3 on page load
if (web3) {
  console.log(`COUNT ADDRESS: ${count_contract_address}`);
  console.log(`ROUND CONTROL ADDRESS: ${round_control_contract_address}`);
  console.log(`REGISTRATION ADDRESS: ${registration_contract_address}`);

  load_registration_contract();
  load_count_contract();
  load_round_control();
} else {
  console.error("Web3 is not initialized. Cannot use Contracts");
}

async function load_registration_contract() {
  let c = new web3.eth.Contract(
    RegistrationArtifact.abi,
    registration_contract_address
  );
  c.handleRevert = true;
  contracts["Registration"] = c;
  console.log(c);

  let list = document.getElementById("dashboardDataParticipantList");
  const val = await c.methods.getRegistrants().call();
  let participants = "";
  for (let i of val) {
    participants += `<tr><td>${i}</td></tr>`;
  }
  list.innerHTML = participants;
}
async function load_count_contract() {
  let c = new web3.eth.Contract(CountArtifact.abi, count_contract_address);
  console.log(c);
  c.handleRevert = true;
  contracts["Count"] = c;

  const subscription = c.events.countChanged();

  document
    .getElementById("countIncrement")
    .addEventListener("click", async () => {
      if (!contracts["Count"] || !connectedAccount) {
        setWarning("Contract / Account is not initialized");
        return;
      }
      try {
        await contracts["Count"].methods.increment().send({
          from: connectedAccount,
        });
      } catch (err) {
        setWarning("TransactionFailed: " + err.message);
      }
    });

  subscription.on("data", (event) => {
    refreshCount(event.returnValues.count);
  });

  let counter = document.getElementById("countDisplay");
  const val = Number(await contracts["Count"].methods.count().call());
  counter.innerText = `Count: ${val}`;
}
async function refreshCount(count) {
  let counter = document.getElementById("countDisplay");
  const val = Number(count);
  counter.innerText = `Count: ${val}`;
}

async function load_round_control(address = "") {
  if (address.length == 0) {
    address = round_control_contract_address;
  }
  let c = new web3.eth.Contract(RoundControlArtificat.abi, address);
  console.log(c);
  c.handleRevert = true;
  contracts["RoundControl"] = c;

  const startSubscription = c.events.RoundStarted();
  const endSubscription = c.events.RoundEnded();
  let setCurrentRound = (val) => {
    let currenRound = document.getElementById("dashboardDataCurrentRound");
    currenRound.innerText = `${val}`;
  };

  startSubscription.on("data", (event) => {
    setCurrentRound(Number(event.returnValues.roundId));
  });
  endSubscription.on("data", (event) => {
    setCurrentRound(Number(event.returnValues.roundId));
  });

  currentRoundId = Number(
    await contracts["RoundControl"].methods.currentRoundId().call()
  );
  setCurrentRound(currentRoundId);

  contracts["RoundControl"].methods
    .owner()
    .call()
    .then((response) => {
      let proposer = document.getElementById("dashboardDataProposer");
      proposer.innerText = response;
    });
  contracts["RoundControl"].methods
    .active()
    .call()
    .then((response) => {
      if (response) {
        const form = document.getElementById("flConfigForm");
        Array.from(form.elements).forEach((el) => (el.disabled = true));
        const proposeSubmitBtn = document.getElementById("proposeSubmitBtn");
        proposeSubmitBtn.innerText = "Round Currently active";
        const deactivateRoundBtn =
          document.getElementById("deactivateRoundBtn");
        deactivateRoundBtn.disabled = false;
        deactivateRoundBtn.style.display = "inline";
      }
    });
}

async function deactivateRound() {
  try {
    await contracts["RoundControl"].methods.endRound().send({
      from: connectedAccount,
    });
    setWarning("Round deactiavted sucessfully", true);
    const proposeSubmitBtn = document.getElementById("proposeSubmitBtn");
    proposeSubmitBtn.innerText = "Start Federated Learning";
    const form = document.getElementById("flConfigForm");
    Array.from(form.elements).forEach((el) => (el.disabled = false));
    const deactivateRoundBtn = document.getElementById("deactivateRoundBtn");
    deactivateRoundBtn.disabled = true;
    deactivateRoundBtn.style.display = "none";
  } catch (err) {
    setWarning("Failed to deactiveate Round: " + err);
  }
}

async function requestAccounts() {
  if (web3 === null) {
    setWarning("Web3 is not initialzed");
    return;
  }

  // await window.ethereum.request({ method: "eth_requestAccounts" });
  // web3 = new Web3(window.ethereum) // Reinitialize web3
  let allAccounts = await web3.eth.getAccounts();
  if (allAccounts.length == 0) {
    setWarning("No Accounts found");
  }
  connectedAccount = allAccounts[0];

  document.getElementById("dashboardDataUserAddress").innerText =
    connectedAccount;
  document.getElementById(
    "accountAddress"
  ).innerHTML = `Connected:<b> ${connectedAccount.slice(
    0,
    5
  )}...${connectedAccount.slice(-5)}</b>`;
  setWarning(`initialized Account: ${connectedAccount}`, true);
}

async function disconnectAccount() {
  if (web3 === null) {
    setWarning("Web3 is not initialzed");
    return;
  }
  connectedAccount = null;
}

async function handleRegister() {
  if (!contracts["Registration"] || !connectedAccount) {
    setWarning("Contract / Account is not initialized");
    return;
  }
  try {
    const tx = await contracts["Registration"].methods
      .register(connectedAccount)
      .send({ from: connectedAccount });

    console.log("Transaction successful:", tx);
    setWarning("Registration successful!", true);
  } catch (error) {
    console.error("Transaction failed", error);
    setWarning("Transaction failed: " + error.message);
  }
}

// Navigation/page switching logic
export function showPage(pageId) {
  document.getElementById("proposerPage").style.display = "none";
  document.getElementById("participantPage").style.display = "none";
  document.getElementById("dashboardPage").style.display = "none";
  document.getElementById(pageId).style.display = "block";
}

// Show proposer page by default on load
showPage("proposerPage");

async function proposeTraining(e) {
  e.preventDefault();
  document.getElementById("proposeSubmitBtn").disabled = true;
  const form = e.target;
  const formData = Object.fromEntries(new FormData(form).entries());

  try {
    await fetch(`/api/propose`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then(async (data) => {
        console.log(data);
        setWarning(`upload model ${data.cid}`, true);

        await contracts["RoundControl"].methods
          .setInitialGlobalModleCid(data.cid)
          .send({
            from: connectedAccount,
          });

        console.log(formData.numClients);
        await contracts["RoundControl"].methods
          .startRound(formData.numClients)
          .send({
            from: connectedAccount,
          });
        await startTraining(formData.numClients, formData.flType, data.cid,formData.epochs);
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("proposeSubmitBtn").disabled = false;
      });
  } catch (err) {
    setWarning("Failed Proposal" + err);
    document.getElementById("proposeSubmitBtn").disabled = false;
  }
  // await fetch(`/api/heartbeat`)
}

async function startTraining(count, flType, cid,rounds) {
  try {
    console.log("Staring rounds: ",rounds)
    for (let round = 1; round < Number(rounds)+1; round++) {

      console.log("rounds ",round)
      const form = new FormData();
      form.append("count", count);
      form.append("flType", flType);
      form.append("cid", cid);
      form.append("round", round);
      const formData = Object.fromEntries(form.entries());

      let result = await (await fetch(`/api/worker/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })).json();

      if (result.cids) {
      const aggegate_form = new FormData();
      aggegate_form.append("flType", flType);
      aggegate_form.append("cids",result.cids);
      aggegate_form.append("round", round);
      const aggegate_formData = Object.fromEntries(aggegate_form.entries());

      let report = await (await fetch(`/api/aggregator/aggregate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(aggegate_formData),
      })).json();
      cid = report.cid
      }
    }
  } catch (err) {
    console.log(err);
    setWarning("Failed Training Initiation" + err);
  }
}

function refreshRoundInfo() {
  let globalModel = document.getElementById("dashboardDataGlobalModel");
  let noOfParticipants = document.getElementById("dashboardDataNoOfClients");
  let currentParticipants = document.getElementById("currentParticipants");
  // if (currentRoundId)
  contracts["RoundControl"].methods
    .getRound(currentRoundId)
    .call()
    .then((response) => {
      if (Number(response) == 0) {
        globalModel.innerText = "N/A";
        noOfParticipants.innerText = "N/A";
        currentParticipants.innerHTML = "";
      } else {
        let c = new web3.eth.Contract(RoundArtificat.abi, response);
        c.methods
          .globalModelCid()
          .call()
          .then((response) => {
            globalModel.innerText = response;
          });
        c.methods
          .getParticipants()
          .call()
          .then((response) => {
            noOfParticipants.innerText = response.length;

            currentParticipants.innerHTML = "";
            for (const p of response) {
              currentParticipants.innerHTML += `<tr><td>${p}</td></tr>`;
            }
          });
      }
    });
  // else {
  //   globalModel.innerText = "N/A";
  //   noOfParticipants.innerText = "N/A";
  //   currentParticipants.innerHTML = "";
  // }
}

window.showPage = showPage;
// window.startFL = startFL;

// Manual refresh for interface
setInterval(() => {
  web3.eth.getBlockNumber().then((response) => {
    let blockHeight = document.getElementById("dashboardDataBlockHeight");
    blockHeight.innerText = Number(response);
  });
  // Show account
  toggleAccountAddress(connectedAccount ? connectedAccount.length != 0 : false);
  refreshRoundInfo();
  contracts["Count"].methods
    .count()
    .call()
    .then((value) => refreshCount(value));
}, 2000);

// async function sendSingedTransaction(contractAddress,contract_interaction){

//    const transactionParameters = {
//       nonce: await web3.eth.getTransactionCount(fromAddress, 'pending'), // Get the next nonce
//       from: fromAddress, // The user's account
//       to: contractAddress, // The address of the contract you're interacting with, or another EOA
//       gas: 0, // Standard gas for simple ETH transfer, adjust for contract calls
//       gasPrice: -1, // Get current gas price
//       data: contract_interaction, // For contract interactions, this would be the encoded function call
//     };

//     const txHash = await web3.request({
//       method: 'eth_sendTransaction',
//       params: [transactionParameters],
//     });

//     const receipt = await web3.eth.waitForTransactionReceipt(txHash);

// }
