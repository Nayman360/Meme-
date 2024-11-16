import requests

def fetch_token_data(contract_address, chain):
    """
    Fetches token details, price, and trading data.
    """
    try:
        print("\n--- Scanning Token Contract ---")
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
        
        # Fetch holders (Solana or Ethereum-specific)
        if chain == "solana":
            solscan_url = f"https://api.solscan.io/token/meta?tokenAddress={contract_address}"
            solscan_data = requests.get(solscan_url).json()
            holders = solscan_data.get('holder_count', "N/A")
            print(f"Number of Holders: {holders}")
        elif chain == "ethereum":
            etherscan_api_key = "YOUR_ETHERSCAN_API_KEY"
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


def analyze_wallet(wallet_address, chain):
    """
    Analyzes a wallet address (e.g., Solana) to determine if it’s good for copy trading.
    """
    try:
        print("\n--- Analyzing Wallet Address ---")
        if chain == "solana":
            # Fetch wallet data from Solscan
            solscan_url = f"https://api.solscan.io/account?address={wallet_address}"
            solscan_data = requests.get(solscan_url).json()

            if solscan_data.get('status', "") != "1":
                print("Wallet address not found or invalid.")
                return None

            token_balances = solscan_data.get('tokenInfo', [])
            total_balance = sum(float(token.get('amount', 0)) for token in token_balances)

            print(f"Wallet Address: {wallet_address}")
            print(f"Total Tokens Held: {len(token_balances)}")
            print(f"Total Balance: {total_balance} SOL")
            print("Top Tokens Held:")
            for token in token_balances[:5]:  # Show top 5 tokens
                print(f"  - {token['tokenAddress']} ({token['amount']} units)")

            print("\nTransaction History:")
            transaction_count = len(solscan_data.get('transactions', []))
            print(f"Total Transactions: {transaction_count}")

            if transaction_count < 50:
                print("Wallet appears inactive, risky for copy trading.")
            else:
                print("Wallet shows good activity, might be worth tracking!")

        elif chain == "ethereum":
            print("Wallet analysis for Ethereum is not implemented yet.")
        else:
            print("Invalid blockchain selection for wallet analysis.")

    except Exception as e:
        print(f"Error analyzing wallet: {e}")


def main():
    """
    Main function for selecting operation mode and executing the appropriate analysis.
    """
    print("Welcome to the Crypto Analysis Tool!")
    print("1. Scan a Token Contract")
    print("2. Analyze a Wallet Address")

    mode = input("Select a mode (1 or 2): ").strip()
    if mode not in ["1", "2"]:
        print("Invalid selection. Exiting.")
        return

    print("\nSelect Blockchain:")
    print("1. Solana")
    print("2. Ethereum")
    blockchain_choice = input("Enter 1 or 2: ").strip()

    if blockchain_choice == "1":
        chain = "solana"
    elif blockchain_choice == "2":
        chain = "ethereum"
    else:
        print("Invalid blockchain selection. Exiting.")
        return

    if mode == "1":
        # Token analysis mode
        contract_address = input("Enter the token contract address: ").strip()
        token_data = fetch_token_data(contract_address, chain)
        if token_data:
            analyze_token(token_data, budget=10)

    elif mode == "2":
        # Wallet analysis mode
        wallet_address = input("Enter the wallet address: ").strip()
        analyze_wallet(wallet_address, chain)


def analyze_token(data, budget=10):
    """
    Analyzes the token based on fetched data and provides trading recommendations.
    """
    if not data:
        print("No data to analyze.")
        return

    print("\n--- Analysis ---")
    price = float(data['price'])
    liquidity = float(data['liquidity'])
    volume = float(data['volume_24h'])
    holders = data['holders']

    print(f"Risk Assessment:")
    if liquidity < 10000:
        print("High risk: Low liquidity may lead to slippage.")
    if holders == "N/A" or int(holders) < 500:
        print("High risk: Few holders indicate a small or inactive community.")

    print("\nInvestment Recommendations:")
    coins_to_buy = budget / price
    print(f"With a ${budget} budget, you can buy approximately {coins_to_buy:.2f} tokens.")
    target_price = price * 1.5
    print(f"Consider selling at a target price of ${target_price:.4f} for a 50% gain.")
    stop_loss = price * 0.8
    print(f"Set a stop-loss at ${stop_loss:.4f} to minimize risk.")


if __name__ == "__main__":
    main()
