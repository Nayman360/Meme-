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
            response = requests.get(solscan_url)
            
            # Handle response errors
            if response.status_code != 200:
                print(f"Error: Solscan API returned status code {response.status_code}.")
                return None
            
            solscan_data = response.json()
            
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
            response = requests.get(dexscreener_url)
            
            # Handle response errors
            if response.status_code != 200:
                print(f"Error: Dexscreener API returned status code {response.status_code}.")
                return None
            
            dexscreener_data = response.json()

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

    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching token data: {e}")
        return None
    except Exception as e:
        print(f"Error fetching token data: {e}")
        return None


def analyze_wallet(address):
    """
    Analyzes a wallet address to check if it's suitable for copy trading (Solana-specific).
    """
    try:
        print("\n--- Analyzing Wallet ---")
        solscan_url = f"https://api.solscan.io/account?address={address}"
        response = requests.get(solscan_url)

        # Handle response errors
        if response.status_code != 200:
            print(f"Error: Solscan API returned status code {response.status_code}.")
            return None
        
        wallet_data = response.json()

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

    except requests.exceptions.RequestException as e:
        print(f"Network error while analyzing wallet: {e}")
        return None
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
        print("Select blockchain:")
        print("1. Solana")
        print("2. Ethereum")
        chain_choice = input("Enter your blockchain choice (1/2): ").strip()
        chain = "solana" if chain_choice == "1" else "ethereum" if chain_choice == "2" else None

        if not chain:
            print("Invalid blockchain selection.")
        else:
            token_data = fetch_token_data(contract_address, chain)
            if token_data:
                print("\n--- Token Analysis Complete ---")

    elif choice == "2":
        wallet_address = input("Enter the wallet address: ").strip()
        analyze_wallet(wallet_address)

    else:
        print("Invalid choice. Exiting.")
