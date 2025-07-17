const hre = require("hardhat");

// scripts/register.js
async function main() {
  const contractAddress = "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512";
  const myContract = await hre.ethers.getContractAt(
    "Registration",
    contractAddress
  );
  const accounts = await hre.ethers.getSigners();
  const randomAccounts = accounts.slice(2,10);

  result = [];
  for (const account of randomAccounts) {
    // Connect contract to the current account
    const tx = await myContract.register(account.address);
    await tx.wait();
    console.log(`Registered: ${account.address}`);
  }
  // result = await myContract.getOwner();
  // result = await myContract.getRandomRegistrant(5)

  const blockNumber = await hre.ethers.provider.getBlockNumber();
  console.log("Current block number:", blockNumber);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
