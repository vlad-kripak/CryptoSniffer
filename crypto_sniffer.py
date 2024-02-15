# CryptoSniffer - monitors Ethereum wallet for large incoming transfers
from web3 import Web3
import requests

INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
WEBHOOK_URL = "https://your.telegram.bot/api/sendMessage"
WATCH_ADDRESS = "0xYourWatchAddress"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def send_alert(amount, tx_hash):
    message = f"Large transfer detected: {w3.fromWei(amount, 'ether')} ETH\nTx: https://etherscan.io/tx/{tx_hash}"
    requests.post(WEBHOOK_URL, data={"chat_id": "@yourchannel", "text": message})

def monitor():
    latest = w3.eth.blockNumber
    while True:
        block = w3.eth.getBlock(latest, full_transactions=True)
        for tx in block.transactions:
            if tx.to and tx.to.lower() == WATCH_ADDRESS.lower():
                if tx.value > w3.toWei(10, 'ether'):  # Threshold 10 ETH
                    send_alert(tx.value, tx.hash.hex())
        latest += 1

if __name__ == "__main__":
    monitor()
