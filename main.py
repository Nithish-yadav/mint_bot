import os
import json
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Web3 connection (replace with your own RPC URL if needed)
RPC_URL = "https://eth-mainnet.public.blastapi.io"  # Free public RPC
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Verify connection
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network. Check your RPC URL.")

# Contract details
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Ensure this is securely stored!

if not CONTRACT_ADDRESS or not PRIVATE_KEY:
    raise Exception("Please set both CONTRACT_ADDRESS and PRIVATE_KEY in the .env file.")

# Load contract ABI (ensure ABI matches the contract's actual ABI)
with open("contract_abi.json") as f:
    contract_abi = json.load(f)

# Set up contract
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

# Function to mint NFT
def mint_nft():
    # Get wallet address from private key
    wallet_address = web3.eth.account.from_key(PRIVATE_KEY).address
    nonce = web3.eth.get_transaction_count(wallet_address)

    # Build transaction
    mint_txn = contract.functions.mint().build_transaction({
        "from": wallet_address,
        "nonce": nonce,
        "gas": 250000,  # Estimated gas limit
        "gasPrice": web3.eth.gas_price  # Current gas price
    })

    # Sign and send transaction
    signed_txn = web3.eth.account.sign_transaction(mint_txn, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Transaction sent! Hash: {web3.to_hex(tx_hash)}")

    # Wait for transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status == 1:
        print("✅ NFT Minted Successfully!")
    else:
        print("❌ Minting Failed")

# Run the script
if __name__ == "__main__":
    try:
        print("[+] Starting NFT Minting Bot...")
        mint_nft()
    except Exception as e:
        print(f"Error: {e}")
