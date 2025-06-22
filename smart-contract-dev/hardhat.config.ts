import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  defaultNetwork: "besu",
  solidity: "0.8.28",
  networks:{
    hardhat:{
    },
    besu:{
      url: "http://127.0.0.1:8541",
      accounts:["0x553602f4273a5488df7cda6be1ac42a5f173061797ac70632d09565555f08d17"]
    }
  }
};

export default config;
