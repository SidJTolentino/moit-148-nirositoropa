from web3 import Web3
import json
import pandas as pd
import time
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
        "name": "rfid",
        "type": "string"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "gpsSensor",
        "type": "string"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "temperatureSensor",
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
        "name": "_rfid",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_gpsSensor",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "_temperatureSensor",
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
        "name": "rfid",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "gpsSensor",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "temperatureSensor",
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
print(f"✅ Connected to Smart Contract at {contract_address}")
print(f"Using default account: {web3.eth.default_account}\n")

df = pd.read_csv("logistics_tracking_data.csv")

print("CSV Preview:")
print(df.head(), "\n")

def send_iot_data(rfid: str, gps_sensor: str, temperature_sensor: str):
    """
    Sends a single IoT data record to the deployed smart contract.
    """
    
    txn = contract.functions.storeData(rfid, gps_sensor, temperature_sensor).transact({
        'from': web3.eth.default_account,
        'gas': 3_000_000
    })
    
    receipt = web3.eth.wait_for_transaction_receipt(txn)
    print(f"✅ Stored | RFID: {rfid} | GPS Sensor: {gps_sensor} | Temp Sensor: {temperature_sensor} | Txn: {receipt.transactionHash.hex()}")


print("⏳ Sending CSV rows to blockchain...\n")
for idx, row in df.iterrows():

    dev_id    = str(row["rfid"])
    dtype     = str(row["gps_sensor"])
    dvalue    = str(row["temperature_sensor"])

    send_iot_data(dev_id, dtype, dvalue)

    time.sleep(1)

print("\n✅ Finished sending all CSV rows.\n")

total_records = contract.functions.getTotalRecords().call()
print(f"Total IoT records stored: {total_records}")

first = contract.functions.getRecord(0).call()
ts0, d0, t0, v0 = first
print("\nFirst stored record:")
print(f"  timestamp: {datetime.datetime.utcfromtimestamp(ts0).strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"  rfid : {d0}")
print(f"  gpsSensor : {t0}")
print(f"  temperatureSensor: {v0}")

last_index = total_records - 1
last = contract.functions.getRecord(last_index).call()
tsL, dL, tL, vL = last
print("\nLast stored record:")
print(f"  timestamp: {datetime.datetime.utcfromtimestamp(tsL).strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"  rfid : {dL}")
print(f"  gpsSensor : {tL}")
print(f"  temperatureSensor: {vL}")
