"""
11. 계정 설정 변경 (AccountSet)

계정의 다양한 플래그를 설정할 수 있습니다.

주요 플래그:
- RequireDestTag: 송금 시 Destination Tag 필수
- RequireAuth: Trust Line 승인 필요
- DisallowXRP: XRP 수신 거부
- etc.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import AccountSet
from xrpl.transaction import submit_and_wait
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== 계정 설정 변경 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed: ").strip()
    wallet = Wallet.from_seed(seed)

    print("설정할 플래그를 선택하세요:")
    print("1. RequireDestTag 설정 (송금 시 Tag 필수)")
    print("2. RequireDestTag 해제")
    choice = input("선택 (1 또는 2): ").strip()

    if choice == "1":
        flag = 0x00020000  # tfRequireDestTag
        print("RequireDestTag 플래그를 설정합니다.")
    elif choice == "2":
        flag = 0x00040000  # tfOptionalDestTag (해제)
        print("RequireDestTag 플래그를 해제합니다.")
    else:
        print("잘못된 선택입니다.")
        return

    if not confirm_action("계정 설정을 변경하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        account_set = AccountSet(
            account=wallet.classic_address,
            set_flag=flag if choice == "1" else None,
            clear_flag=flag if choice == "2" else None,
        )

        print("\n계정 설정 변경 중...")
        response = submit_and_wait(account_set, client, wallet)
        print_transaction_result(response)


if __name__ == "__main__":
    main()