import requests

# Solscan API Key
SOLSCAN_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MzE3NzExNDg3NDgsImVtYWlsIjoia2hzZXJ2aWNlczQxQGdtYWlsLmNvbSIsImFjdGlvbiI6InRva2VuLWFwaSIsImFwaVZlcnNpb24iOiJ2MiIsImlhdCI6MTczMTc3MTE0OH0.N7AVi4SNk_xlkOAsatclAk-ItUnMiWKIZI3c7fLkt4g"

def fetch_token_data(contract_address, chain):
    """
    Fetches token details, price, and trading data.
    """
    try:
        print("\n--- Scanning Token Contract ---")
        if chain == "solana":
            # Use Solscan API for Solana tokens
            solscan_url = f"https://api.solscan.io/token/meta?tokenAddress={contract_address}"
            headers = {"accept": "application/json", "token": SOLSCAN_API_KEY}  # Add API key
            response = requests.get(solscan_url, headers=headers)
            
            if response.status_code == 403:
                print("Error: Access forbidden. Check your Solscan API key.")
                return None
            elif response.status_code != 200:
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
        # Call wallet analysis function (if implemented)
        print("Wallet analysis is currently in development.")
    else:
        print("Invalid choice. Exiting.")
