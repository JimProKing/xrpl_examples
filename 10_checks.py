"""
10. Checks (수표) 기능

Checks는 특정 금액을 나중에 현금화할 수 있는 수표입니다.
수표를 받은 사람은 원할 때 현금화(Cash)할 수 있습니다.

주요 흐름:
1. CheckCreate (수표 발행)
2. CheckCash (수표 현금화)
3. CheckCancel (수표 취소)
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import CheckCreate, CheckCash
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== Checks (수표) 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed (수표 발행자): ").strip()
    wallet = Wallet.from_seed(seed)

    destination = input("수표 수취인 주소: ").strip()
    amount_xrp = float(input("수표 금액 (XRP): ").strip())

    print(f"\n발행자: {wallet.classic_address}")
    print(f"수취인: {destination}")
    print(f"금액: {amount_xrp} XRP")

    if not confirm_action("수표를 발행하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        check_create = CheckCreate(
            account=wallet.classic_address,
            destination=destination,
            send_max=xrp_to_drops(amount_xrp),
        )

        print("\nCheck 생성 중...")
        response = submit_and_wait(check_create, client, wallet)
        result = print_transaction_result(response)

        # Check ID는 메타데이터에서 추출해야 하지만, 간단히 출력
        print("\n수표가 생성되었습니다. Check ID는 트랜잭션 메타데이터에서 확인하세요.")
        print("수취인이 현금화하려면 CheckCash 트랜잭션을 사용합니다.")


if __name__ == "__main__":
    main()