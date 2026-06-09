"""
04. Trust Line 생성

Issued Currency(발행 토큰, 예: USD, EUR 등)를 받거나 보내기 위해서는
먼저 해당 토큰 발행자와 Trust Line(신뢰선)을 맺어야 합니다.

이 예제에서는 특정 발행자와의 Trust Line을 생성합니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import TrustSet
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.transaction import submit_and_wait
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== Trust Line 생성 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed: ").strip()
    wallet = Wallet.from_seed(seed)

    # 예시: 테스트넷에서 자주 사용하는 발행자 주소
    # 실제로는 신뢰할 수 있는 발행자의 주소를 사용해야 합니다.
    issuer = input("토큰 발행자 주소 (Issuer): ").strip()
    currency = input("통화 코드 (예: USD, EUR, FOO): ").strip().upper()
    limit = input("신뢰 한도 (예: 10000): ").strip()

    print(f"\n발신 주소: {wallet.classic_address}")
    print(f"발행자: {issuer}")
    print(f"통화: {currency}")
    print(f"한도: {limit}")

    if not confirm_action("위 내용으로 Trust Line을 생성하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        # TrustSet 트랜잭션 생성
        trust_set = TrustSet(
            account=wallet.classic_address,
            limit_amount=IssuedCurrencyAmount(
                currency=currency,
                issuer=issuer,
                value=limit
            )
        )

        print("\nTrust Line 생성 트랜잭션 제출 중...")
        response = submit_and_wait(trust_set, client, wallet)
        print_transaction_result(response)


if __name__ == "__main__":
    main()