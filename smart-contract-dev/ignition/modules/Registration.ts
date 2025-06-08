import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const RegistrationModule = buildModule("RegistrationModule", (m) => {
  const registration = m.contract("Registration", [], {value:0n});

  return { registration };
});

export default RegistrationModule;