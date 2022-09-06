## Description
A scipt to automate withdrawals from the lending protocol vires.finance. In case of liquidity crisis, the available amount of a stablecoin can most of the time be 0 thus making manual withdrawal very hard. This script automates withdrawal requests and displays relevant information regarding the money withdrawn, the money still on vires, and the amount of waves (token for paying fees) still available.

## Ressources
The main dapp address can be checked at `https://docs.vires.finance/faq/todo-deployed-contracts`. For addresses relative to a particular asset (reserve address, lp token address, and asset address) go to `https://vires.finance/markets` and select the corresponding pool. Finally, lp token prices are displayed et `https://vires.finance/vtokens`.


## Usage
Uptade withdrawal_script.py by selecting your asset (`USDT` or `USDC`), and replacing  `'YOUR_ADDRESS'` and `'YOUR_PRIVATE_KEY'`, by your account address and your private key, respectively.