const hre = require("hardhat");

// scripts/register.js
async function main() {
  const contractAddress = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0";

  // const myContract = await hre.ethers.getContractAt("RoundControl", contractAddress);

  // result = await myContract.createRound(5);
  // console.log(result);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});