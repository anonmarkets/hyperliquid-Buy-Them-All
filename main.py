import json

import utils
import ascii

from hyperliquid.utils import constants


def main():
    # Setup the environment and get the user's address, info, and exchange object
    address, info, exchange = utils.setup(constants.MAINNET_API_URL, skip_ws=True)

    #############################################################
    mcap_filter = "500000"     # Minimum market cap filter
    vol_filter = ""            # Minimum 24h volume filter
    # Use only one of the filters.
    #############################################################
    buy_amount = "10"  # Amount in USDC to spend per token
    # Amount must be over $10!
    #############################################################

    # Retrieve the user's current spot account state
    spot_user_state = info.spot_user_state(address)
    # Extract the available USDC balance from the user's account
    usdc_balance = next((balance['total'] for balance in spot_user_state['balances'] if balance['coin'] == 'USDC'), None)
    print(f"Available USDC balance: {usdc_balance}")

    # Retrieve metadata and asset contexts for spot tokens
    spot_tokens = exchange.info.spot_meta_and_asset_ctxs()

    # Create a mapping from token index to token name
    index_to_name = {token['index']: token['name'] for token in spot_tokens[0]['tokens']}

    # Create a mapping from token index to token details
    index_to_details = {token['index']: token for token in spot_tokens[0]['tokens']}

    # Create a mapping from token name to detailed information
    token_info_map = {}
    universe = spot_tokens[0]['universe']
    market_data = spot_tokens[1]

    # Iterate over market data to populate token information map
    for market in market_data:
        token_name = market['coin']
        universe_entry = None

        if token_name.startswith('@'):
            # Find the corresponding universe entry for tokens with '@' prefix
            universe_entry = next((entry for entry in universe if entry['name'] == token_name), None)
            if universe_entry:
                # Use the first token index to find the actual token name
                token_index = universe_entry['tokens'][0]
                token_name = index_to_name.get(token_index, token_name)

        # Get token details using the index
        token_index = universe_entry['tokens'][0] if universe_entry else None
        token_details = index_to_details.get(token_index, {})

        # Populate the map with detailed information about the token
        token_info_map[token_name] = {
            "id": market['coin'],
            "24h_vol": round(float(market['dayNtlVlm']), 2),
            "price": market['markPx'],
            "mcap": round(float(market['markPx']) * float(market['circulatingSupply']), 2),
            "szDecimals": token_details.get('szDecimals'),
            "weiDecimals": token_details.get('weiDecimals')
        }

    # Manual adjustment for specific token "PURR/USDC"
    if "PURR/USDC" in token_info_map:
        token_info_map["PURR"] = token_info_map.pop("PURR/USDC")
        token_info_map["PURR"]["id"] = "PURR"
        token_info_map["PURR"]["szDecimals"] = 0
        token_info_map["PURR"]["weiDecimals"] = 5

    # Filter out tokens with '@' in their name (failsafe)
    token_info_map = {name: info for name, info in token_info_map.items() if '@' not in name}

    # Initialize a dictionary to hold filtered tokens based on criteria
    filtered_tokens = {}

    # Apply market cap filter if specified
    if mcap_filter and not vol_filter:
        filtered_tokens = {name: info['price'] for name, info in token_info_map.items() if info['mcap'] >= float(mcap_filter)}
    # Apply volume filter if specified
    elif vol_filter and not mcap_filter:
        filtered_tokens = {name: info['price'] for name, info in token_info_map.items() if info['24h_vol'] >= float(vol_filter)}

    # Calculate the total cost of buying the filtered tokens
    total_cost = len(filtered_tokens) * float(buy_amount)
    if total_cost > float(usdc_balance):
        print(f"Your USDC balance must be at least {total_cost} to proceed.")
        # return

    # Create a new map for the amount we can buy per token
    buy_map = {}
    for token_name, price in filtered_tokens.items():
        # Calculate the raw buy amount
        raw_buy_amount = float(buy_amount) / float(price)
        
        # Get the szDecimals for the token
        sz_decimals = token_info_map[token_name].get('szDecimals', 0)
        
        # Round the buy amount according to szDecimals
        buy_map[token_name] = round(raw_buy_amount, sz_decimals)

    # Display the buy map and total cost to the user
    print(buy_map)
    print(f"Following tokens will be bought at a total cost of {total_cost}.\n")

    # Prompt the user for confirmation to proceed with the purchase
    user_input = input("Do you want to proceed? (Y/N): ").strip().upper()
    if user_input not in ['Y', 'y']:
        print("Operation cancelled by the user.")
        return

    # Execute market buy orders for each token in the buy map
    is_buy = True # You can set this to 'False' to market sell all coins
    for token_name, sz in buy_map.items():
        coin = f"{token_name}/USDC"
        print(f"We try to Market {'Buy' if is_buy else 'Sell'} {sz} {coin}.")

        # Place a market order and handle the response
        order_result = exchange.market_open(coin, is_buy, sz, None, 0.01)
        if order_result["status"] == "ok":
            for status in order_result["response"]["data"]["statuses"]:
                try:
                    filled = status["filled"]
                    print(f'Order #{filled["oid"]} filled {filled["totalSz"]} @{filled["avgPx"]}')
                except KeyError:
                    print(f'Error: {status["error"]}')

if __name__ == "__main__":
    ascii.print_ascii_info()
    main()