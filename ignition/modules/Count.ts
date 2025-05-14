import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";


const CountModule = buildModule("CountModule", (m) => {
  const initial_count = m.getParameter("count", 1);

  const count = m.contract("Count", [initial_count], {
    value: 0n,
  });

  return { count };
});

export default CountModule;

// Contract address 0x5FbDB2315678afecb367f032d93F642f64180aa3