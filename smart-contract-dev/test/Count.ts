import { loadFixture } from "@nomicfoundation/hardhat-network-helpers";
import { expect } from "chai";
import hre from "hardhat";

describe("Count",function() {

  async function deployCountFixture() {

    // Contracts are deployed using the first signer/account by default
    const [owner, otherAccount] = await hre.ethers.getSigners();
    const initial_count = 1;

    const Count = await hre.ethers.getContractFactory("Count");
    const count = await Count.deploy(initial_count);

    return { count, initial_count, owner, otherAccount };
  }

    describe("Count Basics", function(){

        it( "Constructor Call",async function(){
            const { count ,initial_count} = await loadFixture(deployCountFixture);
            expect(await count.count()).to.equal(initial_count);
        });


        it( "increment",async function(){
            const { count ,initial_count} = await loadFixture(deployCountFixture);
            await count.increment();
            expect(await count.count()).to.equal(initial_count + 1);
        });
    });
});