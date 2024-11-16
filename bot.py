import requests


def fetch_token_data(contract_address, chain):
    """
    Fetches token details, price, and trading data.
    """
    try:
        print("\n--- Scanning Token Contract ---")
        if chain == "solana":
            # Use Solscan API for Solana tokens
            solscan_url = f"https://api.solscan.io/token/meta?tokenAddress={contract_address}"
            solscan_data = requests.get(solscan_url).json()

            if "status" in solscan_data and solscan_data["status"] != 1:
                print("Token not found on Solscan. Verify the address and try again.")
                return None

            token_name = solscan_data.get("name", "N/A")
            symbol = solscan_data.get("symbol", "N/A")
            holders = solscan_data.get("holder_count", "N/A")
            print(f"Token Name: {token_name}")
            print(f"Symbol: {symbol}")
            print(f"Number of Holders: {holders}")

            return {
                "name": token_name,
                "symbol": symbol,
                "holders": holders,
            }

        elif chain == "ethereum":
            # Use Dexscreener for Ethereum tokens
            dexscreener_url = f"https://api.dexscreener.io/latest/dex/tokens/{contract_address}"
            dexscreener_data = requests.get(dexscreener_url).json()

            if "pair" not in dexscreener_data:
                print("Token not found on Dexscreener. Verify the address and try again.")
                return None

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

            return {
                "price": price,
                "liquidity": liquidity,
                "volume_24h": volume_24h,
                "price_change_24h": price_change_24h,
            }

        else:
            print("Unsupported blockchain. Only 'solana' and 'ethereum' are supported.")
            return None

    except Exception as e:
        print(f"Error fetching token data: {e}")
        return None


def analyze_token(data, budget=10):
    """
    Analyzes the token based on fetched data and provides trading recommendations.
    """
    if not data:
        print("No data to analyze.")
        return

    print("\n--- Analysis ---")
    if "price" in data:
        price = float(data['price'])
        liquidity = float(data['liquidity'])
        volume = float(data['volume_24h'])

        print(f"Risk Assessment:")
        if liquidity < 10000:
            print("High risk: Low liquidity may lead to slippage.")
        if "holders" in data and (data["holders"] == "N/A" or int(data["holders"]) < 500):
            print("High risk: Few holders indicate a small or inactive community.")

        print("\nInvestment Recommendations:")
        coins_to_buy = budget / price
        print(f"With a ${budget} budget, you can buy approximately {coins_to_buy:.2f} tokens.")
        target_price = price * 1.5  # Example target: 50% gain
        print(f"Consider selling at a target price of ${target_price:.4f} for a 50% gain.")
        stop_loss = price * 0.8  # Example stop-loss: 20% loss
        print(f"Set a stop-loss at ${stop_loss:.4f} to minimize risk.")
    else:
        print(f"Token Name: {data['name']}")
        print(f"Symbol: {data['symbol']}")
        print(f"Number of Holders: {data['holders']}")


def analyze_wallet(address):
    """
    Analyzes a wallet address to check if it's suitable for copy trading (Solana-specific).
    """
    try:
        print("\n--- Analyzing Wallet ---")
        solscan_url = f"https://api.solscan.io/account?address={address}"
        wallet_data = requests.get(solscan_url).json()

        if "status" in wallet_data and wallet_data["status"] != 1:
            print("Wallet not found on Solscan. Verify the address and try again.")
            return None

        tx_count = wallet_data.get("tx_count", 0)
        balance = wallet_data.get("balance", {}).get("total", 0)
        print(f"Wallet Address: {address}")
        print(f"Transaction Count: {tx_count}")
        print(f"Total Balance: {balance} SOL")

        # Evaluate based on activity
        if tx_count > 100:
            print("This wallet has high activity and may belong to an experienced trader.")
        else:
            print("This wallet has low activity. Be cautious when copying trades.")

        return wallet_data

    except Exception as e:
        print(f"Error analyzing wallet: {e}")
        return None


if __name__ == "__main__":
    print("Select an option:")
    print("1. Scan a token contract")
    print("2. Analyze a wallet address")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        contract_address = input("Enter the token contract address: ").strip()
        chain = input("Enter the blockchain (solana/ethereum): ").strip().lower()
        token_data = fetch_token_data(contract_address, chain)
        if token_data:
            analyze_token(token_data, budget=10)

    elif choice == "2":
        wallet_address = input("Enter the wallet address: ").strip()
        analyze_wallet(wallet_address)

    else:
        print("Invalid choice. Exiting.")
