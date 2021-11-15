# Simple Price Oracle

## Summary

This simple price oracle consists of two main components

### Oracle CosmWasm smart contract

The contract can store the price data that originates from data requests made by the off-chain service and sent to this contract on Terra. More details [here](oracle-smart-contract/README.md).

### Off-chain service

This service will be responsible for aggregating prices from sources and sending price update transactions to the smart contract above on Terra. More details [here](off-chain-service/README.md).


## Further improvements

In my opinion, this service can be improved by implementing following modules/functions.

### Oracle contract
- Security: access control and ownership in some methods such as `set_price` to prevent unauthorized update of the price.
- Efficiency: implements batch or array-like `set_price` and `get_price` methods to maximize gas efficiency when writing or reading the contract state.
