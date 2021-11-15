# Off-chain Service

## Summary

The service consists of two applications `feeder` and `server`

### Feeder

<img width="600" alt="feeder" src="https://user-images.githubusercontent.com/42636319/141781620-edc4b967-47bf-4b43-b5b0-8ea2c89a8dc4.png">

This application is responsible for getting the aggregated price from the `server` to be updated on the blockchain by sending an `ExecuteMsg` transaction to the Terra wasm module.

The feeder also checks for returned values from the contract. If there is no matching symbol found on the contract, it will handle this case by sending the price without checking with the price deviation rule as if it is creating a new symbol on the contract state.

### Server

<img width="600" alt="Screen Shot 2564-11-15 at 3 36 08 PM" src="https://user-images.githubusercontent.com/42636319/141781800-1e0e283b-8d53-4d5d-b250-253d45b71445.png">

This server will automatically fetch the latest price from two sources, `CoinGecko` and `Binance`. Then save the aggregated price every 30 seconds. Also, the latest price can be requested from this server via `http://127.0.0.1:8000/latest`.


## How to run the service

### Dependencies Installation

Run the following commands inside this directory `off-chain-service`.
```shell
python3 -m pip install pipenv
pipenv install
pipenv shell
```

### Run the server
```shell
cd server
uvicorn app:app
```

### Then run the feeder
```shell
cd feeder
python3 main.py
```
