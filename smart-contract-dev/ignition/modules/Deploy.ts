import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const FeduntuModule = buildModule("FeduntuModule", (m) => {
  // Accept initialGlobalModelCid as a parameter when running the module
  const initialGlobalModelCid = 'QmPXwmjJzQpG3cNc1b5qa9pPQZ3vp5TbNYa5pgfrCamkL7' 
  // m.getParameter("initialGlobalModelCid", "QmDefaultCID");

  const count = m.contract("Count",[1]);
  // Deploy Registration contract
  const registration = m.contract("Registration");
  // Deploy RoundControl contract with dynamic CID and registration address
  console.log(initialGlobalModelCid)
  const roundControl = m.contract("RoundControl", [
    initialGlobalModelCid,
    registration,
  ]);

  return { registration, roundControl , count };
});

export default FeduntuModule;
