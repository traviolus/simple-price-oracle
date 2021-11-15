use cw_storage_plus::Map;
use cosmwasm_std::Uint128;

pub const PRICE_MAP: Map<String, Uint128> = Map::new("price_map");
