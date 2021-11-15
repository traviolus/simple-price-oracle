#[cfg(not(feature = "library"))]
use cosmwasm_std::entry_point;
use cosmwasm_std::{to_binary, Binary, Deps, DepsMut, Env, MessageInfo, Response, StdResult, Uint128, StdError};
use cw2::set_contract_version;

use crate::error::ContractError;
use crate::msg::{GetPriceResponse, ExecuteMsg, InstantiateMsg, QueryMsg};
use crate::state::PRICE_MAP;

// version info for migration info
const CONTRACT_NAME: &str = "crates.io:oracle-smart-contract";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    _msg: InstantiateMsg,
) -> Result<Response, ContractError> {
    set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;
    Ok(Response::new()
        .add_attribute("method", "instantiate")
        .add_attribute("owner", info.sender)
    )
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg {
        ExecuteMsg::SetPrice { symbol, price } => try_set_price(deps, symbol, price),
    }
}

pub fn try_set_price(deps: DepsMut, symbol: String, price: Uint128) -> Result<Response, ContractError> {
    PRICE_MAP.save(deps.storage, symbol, &price)?;
    Ok(Response::new().add_attribute("method", "try_set_price"))
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    match msg {
        QueryMsg::GetPrice { symbol } => to_binary(&query_price(deps, symbol)?),
    }
}

fn query_price(deps: Deps, symbol: String) -> StdResult<GetPriceResponse> {
    match PRICE_MAP.may_load(deps.storage, symbol) {
        Ok(Some(price)) => Ok(GetPriceResponse { price }),
        Ok(None) => Err(StdError::NotFound { kind: "Price".to_string() }),
        Err(e) => Err(e),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info};
    use cosmwasm_std::from_binary;

    #[test]
    fn initialization() {
        let mut deps = mock_dependencies(&[]);

        let msg = InstantiateMsg {};
        let info = mock_info("creator", &[]);

        let res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();
        assert_eq!(0, res.messages.len());
    }

    #[test]
    fn set_price() {
        let mut deps = mock_dependencies(&[]);

        let msg = InstantiateMsg {};
        let info = mock_info("creator", &[]);
        let _res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();

        let info = mock_info("anyone", &[]);
        let msg = ExecuteMsg::SetPrice { symbol: "LUNA".to_string(), price: Uint128::from(51280000000u64) };
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();

        let res = query(deps.as_ref(), mock_env(), QueryMsg::GetPrice { symbol: "LUNA".to_string() }).unwrap();
        let value: GetPriceResponse = from_binary(&res).unwrap();
        assert_eq!(Uint128::from(51280000000u64), value.price);
    }

    #[test]
    fn get_non_available_price() {
        let mut deps = mock_dependencies(&[]);

        let msg = InstantiateMsg {};
        let info = mock_info("creator", &[]);
        let _res = instantiate(deps.as_mut(), mock_env(), info, msg).unwrap();

        let info = mock_info("feeder", &[]);
        let msg = ExecuteMsg::SetPrice { symbol: "ETH".to_string(), price: Uint128::from(4710990000000u64) };
        let _res = execute(deps.as_mut(), mock_env(), info, msg).unwrap();

        let res = query(deps.as_ref(), mock_env(), QueryMsg::GetPrice { symbol: "LUNA".to_string() });
        assert_eq!(res.unwrap_err(), StdError::NotFound { kind: "Price".to_string() })
    }
}
