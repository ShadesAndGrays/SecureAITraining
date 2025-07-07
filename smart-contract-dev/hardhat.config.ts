import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  defaultNetwork: "besu",
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
      evmVersion: "london",
    },
  },
  networks: {
    hardhat: {},
    besu: {
      url: "http://192.168.1.2:8541",
      gasPrice: 0,
      gas: -1,
      accounts: [
        "0x553602f4273a5488df7cda6be1ac42a5f173061797ac70632d09565555f08d17",
        "0x7d3fe475e367ae5a94b1340856e4ab58d9dcd38803c740b9166aaa4b59225546",
      ],
    },
  },
};

export default config;
