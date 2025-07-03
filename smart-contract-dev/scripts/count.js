const hre = require("hardhat");

// scripts/register.js
async function main() {
  const contractAddress = "0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82";
  const myContract = await hre.ethers.getContractAt("Count", contractAddress);
  const account = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
  // const txResult = await myContract.register("0xE1f69F3ca3D2983cb622458b405024daA934aa24");
  // console.log(txResult);
  await myContract.increment()
  const result = await myContract.count()
  // const result = await myContract.isValid("0xE1f69F3ca3D2983cb622458b405024daA934aa24");
  // const result = await myContract.getOwner();
  console.log(result);

}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});