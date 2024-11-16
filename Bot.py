import requests

def fetch_token_data(contract_address, chain="solana"):
    """
    Fetches token details, price, and trading data from Dexscreener and blockchain explorers.

    Args:
        contract_address (str): The contract address of the token.
        chain (str): Blockchain where the token is deployed (default: solana).

    Returns:
        dict: Token data including price, volume, holders, and liquidity.
    """
    try:
        # Fetch token details from Dexscreener
        dexscreener_url = f"https://api.dexscreener.io/latest/dex/tokens/{contract_address}"
        dexscreener_data = requests.get(dexscreener_url).json()

        if "pair" not in dexscreener_data:
            print("Token not found on Dexscreener.")
            return None

        # Extract relevant details
        token_data = dexscreener_data['pair']
        price = token_data['priceUsd']
        liquidity = token_data['liquidity']['usd']
        volume_24h = token_data['volume']['h24']
        price_change_24h = token_data['priceChange']['h24']

        print(f"Token Address: {contract_address}")
        print(f"Price (USD): ${price}")
        print(f"Liquidity (USD): ${liquidity}")
        print(f"24h Volume (USD): ${volume_24h}")
        print(f"24h Price Change: {price_change_24h}%")
        
        # Fetch holders from Solscan (Solana-specific)
        if chain == "solana":
            solscan_url = f"https://api.solscan.io/token/meta?tokenAddress={contract_address}"
            solscan_data = requests.get(solscan_url).json()
            holders = solscan_data.get('holder_count', "N/A")
            print(f"Number of Holders: {holders}")

        # Fetch holders from Etherscan (Ethereum-specific)
        elif chain == "ethereum":
            etherscan_api_key = "YOUR_ETHERSCAN_API_KEY"  # Replace with your API key
            etherscan_url = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={contract_address}&apikey={etherscan_api_key}"
            etherscan_data = requests.get(etherscan_url).json()
            holders = etherscan_data.get('result', "N/A")
            print(f"Number of Holders: {holders}")

        return {
            "price": price,
            "liquidity": liquidity,
            "volume_24h": volume_24h,
            "price_change_24h": price_change_24h,
            "holders": holders,
        }

    except Exception as e:
        print(f"Error fetching token data: {e}")
        return None


def analyze_token(data, budget=10):
    """
    Analyzes the token based on fetched data and provides trading recommendations.

    Args:
        data (dict): Token data fetched from APIs.
        budget (float): Budget in USD for investment.

    Returns:
        None
    """
    if not data:
        print("No data to analyze.")
        return

    print("\n--- Analysis ---")
    price = float(data['price'])
    liquidity = float(data['liquidity'])
    volume = float(data['volume_24h'])
    holders = data['holders']

    # Risk assessment
    print(f"Risk Assessment:")
    if liquidity < 10000:
        print("High risk: Low liquidity may lead to slippage.")
    if holders == "N/A" or int(holders) < 500:
        print("High risk: Few holders indicate a small or inactive community.")

    # Investment recommendations
    print("\nInvestment Recommendations:")
    coins_to_buy = budget / price
    print(f"With a ${budget} budget, you can buy approximately {coins_to_buy:.2f} tokens.")
    target_price = price * 1.5  # Example target: 50% gain
    print(f"Consider selling at a target price of ${target_price:.4f} for a 50% gain.")
    stop_loss = price * 0.8  # Example stop-loss: 20% loss
    print(f"Set a stop-loss at ${stop_loss:.4f} to minimize risk.")

    # Conclusion
    print("\nTrade cautiously and monitor price movements closely!")


# Example Usage
if __name__ == "__main__":
    contract_address = input("Enter the contract address of the token: ").strip()
    chain = input("Enter the blockchain (solana/ethereum): ").strip().lower()

    token_data = fetch_token_data(contract_address, chain)
    if token_data:
        analyze_token(token_data, budget=10)
