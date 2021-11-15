from time import sleep
from typing import Union
from terra_sdk.client.lcd import LCDClient
from terra_sdk.core.auth import StdFee
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.core import Coins, AccAddress
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.exceptions import LCDResponseError
import requests


terra = LCDClient(chain_id="bombay-12", url="https://bombay-lcd.terra.dev")
contract_address = AccAddress("terra1ut9gfm008p8caun3dlgt2tn2p7pkrjaw5qexw3")
sender_account = terra.wallet(MnemonicKey(
    "inherit taxi deposit fabric hockey time shift miss nut spare nominee record gun fashion among install trade episode appear exclude debris patch idea weapon"))
max_deviation_threshold = 0.001  # 0.1%


def max_deviation(a: float, b: float) -> float:
    return abs(a-b)/min(a, b)


def get_execute_msg(symbol: str, price: float) -> Union[MsgExecuteContract, None]:
    try:
        query_result = terra.wasm.contract_query(
            contract_address,
            {"get_price": {"symbol": symbol}}
        )
        query_price = float(query_result["price"]) / 1000000000
        print(f"[{symbol}] query price: {query_price}\treal price: {price}\tdeviation: {round(max_deviation(query_price, price)*100, 4)}%")
        if max_deviation(query_price, price) <= max_deviation_threshold:
            return None
    except LCDResponseError as e:
        if "Price not found" in str(e):
            print(f"new price feed [symbol: {symbol}, price: {price}]")
            pass
        else:
            raise e
    multiplied_price = str(int(price*1000000000))
    execute_msg = MsgExecuteContract(
        sender_account.key.acc_address,
        contract_address,
        {"set_price": {"symbol": symbol, "price": multiplied_price}},
        Coins(),
    )
    return execute_msg


def send_set_price_tx() -> None:
    response = requests.get("http://127.0.0.1:8000/latest").json()
    execute_msgs = []
    for symbol in response:
        msg = get_execute_msg(symbol, response[symbol])
        if msg is None:
            continue
        execute_msgs.append(msg)

    if execute_msgs:
        execute_tx = sender_account.create_and_sign_tx(
            msgs=execute_msgs,
            fee=StdFee(300000, Coins("100000uluna")),
        )
        execute_tx_result = terra.tx.broadcast(execute_tx)
        print(f"Tx hash: {execute_tx_result.txhash}")


if __name__ == "__main__":
    while True:
        send_set_price_tx()
        print("----------------------------------------------------------------------------")
        sleep(30)
