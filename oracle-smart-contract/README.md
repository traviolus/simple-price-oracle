# Oracle CosmWasm Smart Contract

## Code Breakdown
Here is the breakdown of the oracle smart contract. The contract can be broken down into 3 sections which are `messages`, `state` and `contract logic`.

### Messages

The `InstantiateMsg` is used to instantiate the contract and its states. Thus, it will only be executed once. This contract does not have any initial state so the `InstantiateMsg` looks like this.

```rust
pub struct InstantiateMsg {}
```

Next, the `ExecuteMsg` is used for state transition of the contract. For this contract we only have one sub message, `SetPrice`. It is used when the feeder wants to update the price of one single symbol.
```rust
pub enum ExecuteMsg {
    SetPrice { symbol: String, price: Uint128 },
}
```

Finally we have the `QueryMsg`, it is used for contract state reading. This message also has one sub message, `GetPrice`. The messages will be used to read the price of a specific symbol.
```rust
pub enum QueryMsg {
    GetPrice { symbol: String },
}
```

### State

This contract only contains one `PRICE_MAP` state which is a `Map` (String => Uint128) being used to store symbol to price mapping.

```rust
pub const PRICE_MAP: Map<String, Uint128> = Map::new("price_map");
```

### Contract Logic

The contract logic can be divided into three parts which are `instantiate`, `execute` and `query`.

The `instantiate` part is only used at the contract instantiation step. It just sets the contract name and version according to [CW2](https://github.com/CosmWasm/cw-plus/blob/main/packages/cw2/README.md) spec.

The `execute` part will try to update the new price to the state and raise errors if needed.

The `query` part basically try to query for the given symbol. Returns its price if there exists the given symbol or otherwise return `StdError::NotFound`.

## Deployed Contract

### Testnet Bombay-12

| Contract | Address |
|----------|---------|
| Oracle smart contract | [terra1ut9gfm008p8caun3dlgt2tn2p7pkrjaw5qexw3](https://finder.terra.money/testnet/address/terra1ut9gfm008p8caun3dlgt2tn2p7pkrjaw5qexw3) |

