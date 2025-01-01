# Hyperliquid Buy-Them-All

## Overview

The Hyperliquid Buy-Them-All is a Python-based tool designed to automate the purchase of every spot token available on the Hyperliquid platform. This tool allows users to set specific criteria to exclude tokens with low market cap or low trading volume, thereby avoiding tokens with potentially high spreads which can result in market buys with extremly high markup. Users can also specify a fixed amount to invest in each token which is then bought via market orders.


## Features

- **Automated Token Purchase**: Automatically buys every spot token on Hyperliquid.
- **Exclusion Criteria**: Set criteria to exclude tokens with low market capitalization or low trading volume.
- **Fixed Investment Amount**: Specify a fixed amount (min. $10) to invest in each token.
- **User-Friendly Configuration**: Easily configure the criteria and investment amount via variables.

## Installation

Make sure you have Python 3.10+ installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/anonmarkets/hyperliquid-Buy-Them-All.git
   ```
2. Navigate to the project directory:
   ```bash
   cd hyperliquid-Buy-Them-All
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Create a new API key at [Hyperliquid API](https://app.hyperliquid.xyz/API).

2. Open the `config.json` file and paste your secret key and wallet address (not the agent wallet address):
   ```json
   {
     "secret_key": "your API secret key",
     "account_address": "your wallet address"
   }
   ```

3. Configure the parameters in the script by setting `mcap_filter`, `vol_filter`, and `buy_amount` to your desired values.

4. Run the script:
   ```bash
   python main.py
   ```

5. Confirm the purchase when prompted by the script.

_Side note: You can set `is_buy` to `False` to market sell these coins again (we both know you won't use this)._


## License

This project is licensed under the MIT License.

## Contact

X: https://x.com/anonmarkets

___

If you like this project support me by using my ref links:

- Hyperliquid: https://app.hyperliquid.xyz/join/ANONMARKETS
- pvp.trade: https://pvp.trade/join/xiere1
- HypurrFun: https://t.me/HypurrFunBot?start=ref_6869d609
- Donation: 0xB2cef143Bea4FF180Fe2831932B4da04c3259333
___

_P.S. This tool is built using example code from the Hyperliquid SDK. I didn't invest much time in developing it, so it currently operates as a CLI application. Yes, this readme is AI generated._


Hyperliquid.
