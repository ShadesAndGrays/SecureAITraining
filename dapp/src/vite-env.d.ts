/// <reference types="vite/client" />

// <reference types="react-scripts" />
import { MetaMaskProvider } from 'web3';

declare global {
	interface Window {
		ethereum: MetaMaskProvider;
	}
}