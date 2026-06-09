"""
05. Issued Currency 송금

Trust Line이 이미 설정되어 있다면, 발행 토큰(USD, EUR 등)을 송금할 수 있습니다.

이 예제는 04_trustline.py 이후에 실행하는 것을 추천합니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.transaction import submit_and_wait
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== Issued Currency 송금 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed: ").strip()
    wallet = Wallet.from_seed(seed)

    destination = input("수신 주소: ").strip()
    issuer = input("토큰 발행자 주소: ").strip()
    currency = input("통화 코드 (예: USD): ").strip().upper()
    amount = input("송금 수량: ").strip()

    print(f"\nFrom: {wallet.classic_address}")
    print(f"To  : {destination}")
    print(f"Amount: {amount} {currency} (Issuer: {issuer})")

    if not confirm_action("위 내용으로 Issued Currency를 송금하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        payment = Payment(
            account=wallet.classic_address,
            destination=destination,
            amount=IssuedCurrencyAmount(
                currency=currency,
                issuer=issuer,
                value=amount
            )
        )

        print("\nIssued Currency 송금 중...")
        response = submit_and_wait(payment, client, wallet)
        print_transaction_result(response)


if __name__ == "__main__":
    main()