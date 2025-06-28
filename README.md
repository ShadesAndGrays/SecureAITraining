# Secure AI Training Project

This project is the final year work of Clement Obieke, submitted in partial fulfillment of the requirements for the Bachelor of Computer Science, under the supervision of Dr. Pius Onobhayedo.

---

## Project Overview

**Secure AI Training** is a decentralized federated learning platform that leverages blockchain and smart contracts to coordinate collaborative AI model training while preserving data privacy through the use of Federated learning techniques.

---

## Project Structure

The project is organized into four main components:

### 1. Decentralized Application (DApp)
- **Frontend:** Built with JavaScript, HTML, and CSS (React + Vite), the DApp provides the user interface for interacting with the system.
- **Features:**
  - User registration and authentication (via wallet integration, e.g., MetaMask)
  - Real-time monitoring of training progress
  - Listening to blockchain events (e.g., eligibility, model updates)
  - Fetching the global model CID from the blockchain

### 2. Python Client
  - Handles local AI model training on user data
  - Exposes a Flask server for the DApp to communicate with Python code, enabling seamless integration of data science workflows

### 3. Smart Contract Development
- **Purpose:** Implements core logic on the blockchain for transparency and trustlessness.
- **On-chain Logic:**
  - Client selection
  - Aggregation coordination
  - Reputation and incentive mechanisms
  - Registration and banning of clients

### 4. Blockchain and IPFS
- **Blockchain:** Hosts smart contracts and records key events and metadata.
- **IPFS:** Used for decentralized storage of model weights and artifacts. The project will evaluate whether sensitive data can be securely stored on-chain or if IPFS is required for privacy and scalability.
- **Pinning Services:** Use IPFS pinning services (like Pinata, Infura, or your own node) to ensure files are always available and propagate faster.
- **Hybrid Storage:** Consider using a CDN or centralized storage alongside IPFS. Centralization can improve speed and reliability, while IPFS provides hash-based lookup and auditability.

Considerations:
- **Timeouts:** Implement timeouts for unavailable users to prevent rounds from stalling.
- **Pre-fetching:** Encourage participants to pre-fetch the global model before the round starts to reduce waiting time.
---

## Usage

### Decentralized Application (DApp)

1. Run the React app via Vite.
2. Register using your MetaMask wallet.
3. A local Python server is used on the client side to train the local model and interact with the DApp.

### Smart Contract Development

To run the test node with Hardhat:

```bash
cd smart-contract-dev
npm run launch:dev
```

---

## Additional Notes

- All components are designed to be dockerized for easy deployment and reproducibility.
- See [`TODO.md`](TODO.md) for a detailed breakdown of planned features and progress.
- For API documentation and further setup instructions, refer to the respective `README.md` files in each subdirectory.

## Prospective Datasets

[Email Spam](https://www.kaggle.com/datasets/purusinghvi/email-spam-classification-dataset)
[Extended MNIST](https://www.kaggle.com/datasets/crawford/emnist)
[California Housing](https://www.kaggle.com/datasets/camnugent/california-housing-prices)