import { connectorsForWallets } from '@rainbow-me/rainbowkit';
import { coinbaseWallet, injectedWallet, rainbowWallet, walletConnectWallet } from '@rainbow-me/rainbowkit/wallets';
import { createConfig, http } from 'wagmi';
import { defineChain } from 'viem';
import { metaMaskInjectedWallet } from './metaMaskInjectedWallet';

const projectId = process.env.REACT_APP_WALLETCONNECT_PROJECT_ID;
const chainId = Number(process.env.REACT_APP_ROBINHOOD_CHAIN_ID);
const rpcUrl = process.env.REACT_APP_ROBINHOOD_RPC_URL;
const explorerUrl = process.env.REACT_APP_ROBINHOOD_EXPLORER_URL;
const appUrl = process.env.REACT_APP_BACKEND_URL;

if (!projectId || !rpcUrl || !explorerUrl || !appUrl || chainId !== 4663) {
  throw new Error('Wallet configuration requires a Reown project ID and Robinhood Mainnet (4663) environment settings.');
}

export const robinhoodMainnet = defineChain({
  id: chainId,
  name: 'Robinhood Chain',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: { default: { http: [rpcUrl] } },
  blockExplorers: { default: { name: 'Robinhood Explorer', url: explorerUrl } },
});

const connectors = connectorsForWallets([
  { groupName: 'Wallets', wallets: [metaMaskInjectedWallet, rainbowWallet, coinbaseWallet, walletConnectWallet] },
  { groupName: 'Browser wallets', wallets: [injectedWallet] },
], { appName: 'LastZHood', appUrl, projectId });

export const wagmiConfig = createConfig({
  chains: [robinhoodMainnet],
  connectors,
  transports: { [robinhoodMainnet.id]: http(rpcUrl) },
  multiInjectedProviderDiscovery: true,
  ssr: false,
});