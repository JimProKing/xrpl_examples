"""
06. DEX (탈중앙화 거래소) 오퍼 생성

XRPL의 내장 DEX에 매수 또는 매도 오퍼를 등록할 수 있습니다.

이 예제에서는 XRP를 특정 Issued Currency와 교환하는 오퍼를 만듭니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import OfferCreate
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== DEX Offer 생성 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed: ").strip()
    wallet = Wallet.from_seed(seed)

    # 예: 1 XRP = 0.5 USD 로 매도 오퍼 생성
    taker_gets_currency = "XRP"           # 내가 주는 것
    taker_gets_value = input("매도할 XRP 수량: ").strip()

    taker_pays_issuer = input("받을 토큰 발행자: ").strip()
    taker_pays_currency = input("받을 토큰 코드 (예: USD): ").strip().upper()
    taker_pays_value = input("받고 싶은 토큰 수량: ").strip()

    print(f"\n매도: {taker_gets_value} XRP")
    print(f"매수: {taker_pays_value} {taker_pays_currency} @ {taker_pays_issuer}")

    if not confirm_action("위 내용으로 DEX 오퍼를 생성하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        offer = OfferCreate(
            account=wallet.classic_address,
            taker_gets=xrp_to_drops(taker_gets_value),  # XRP는 drops로
            taker_pays=IssuedCurrencyAmount(
                currency=taker_pays_currency,
                issuer=taker_pays_issuer,
                value=taker_pays_value
            )
        )

        print("\nDEX 오퍼 생성 중...")
        response = submit_and_wait(offer, client, wallet)
        print_transaction_result(response)


if __name__ == "__main__":
    main()