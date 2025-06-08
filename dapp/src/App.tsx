import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [input, setInput] = useState(1)
  const [count, setCount] = useState(1);

   let getFactorial = () =>{
    fetch(`http://localhost:5000/calculate?number=${input}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            setCount(Number(data.result));
            })
        .catch(error => console.error('Error:', error));
}
  return (
    <>
      <div>
        <label >Input: </label>
        <input
        type="number"
        value={input}
        onChange={e => setInput(Number(e.target.value))}
        />

        <h1> Federated Day </h1>
        <p>This page would be used to regeister the user to the dapp</p>
        <button onClick={() => getFactorial()}> Click me </button>
        <p> Count: {count}</p>
      </div>

      {/* <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
    </>
  );
}

export default App;
