from web3 import Web3
import json
import datetime

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("❌ Could not connect. Make sure Ganache is running.")
    exit(1)
print("✅ Connected to Ganache.")

contract_address = "0x1d7aF1c683F8093A4baBE4B7Ee5D5E1ebeb8C063"

abi_json = """
[
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "deviceId",
        "type": "string"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "dataType",
        "type": "string"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "dataValue",
        "type": "string"
      }
    ],
    "name": "DataStored",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "_deviceId",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_dataType",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_dataValue",
        "type": "string"
      }
    ],
    "name": "storeData",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "dataRecords",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "deviceId",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "dataType",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "dataValue",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "index",
        "type": "uint256"
      }
    ],
    "name": "getRecord",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalRecords",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "MAX_ENTRIES",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
"""
abi = json.loads(abi_json)

contract = web3.eth.contract(address=contract_address, abi=abi)

web3.eth.default_account = web3.eth.accounts[0]
print(f"✅ Loaded contract at {contract_address}")
print(f"Using default account: {web3.eth.default_account}")

total_before = contract.functions.getTotalRecords().call()
print("Total records before storing data:", total_before)

for i in range(5):
    device_id = f"TEST{i+1:03d}"
    data_type = "Temperature"
    data_value = f"{20 + i*0.5}°C"
    print(f"Storing entry #{i+1}: {device_id}, {data_type}, {data_value}")
    txn = contract.functions.storeData(device_id, data_type, data_value).transact({
        "from": web3.eth.default_account,
        "gas": 200_000
    })
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"  → Mined in tx: {receipt.transactionHash.hex()}\n")

total_after = contract.functions.getTotalRecords().call()
print("Total records after storing data:", total_after)

print("\nRetrieving all stored records:")
for idx in range(total_after):
    ts, dev, dtype, dval = contract.functions.getRecord(idx).call()
    readable = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"Record {idx}: time={readable}, deviceId={dev}, type={dtype}, value={dval}")
