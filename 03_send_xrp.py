"""
03. XRP 송금 (Payment - XRP)

가장 기본적인 기능입니다.
한 계정에서 다른 계정으로 XRP를 보냅니다.

이 예제는 이전에 만들었던 송금 스크립트를 초보자 친화적으로 재구성한 버전입니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops
from common import get_client, TESTNET_URL, get_account_balance, print_transaction_result, confirm_action


def main():
    print("=== XRP 송금 예제 (테스트넷) ===\n")

    client = get_client(TESTNET_URL)

    # 1. 발신 지갑 정보 입력
    print("발신 계정 정보를 입력하세요.")
    seed = input("Seed (s로 시작하는 비밀키): ").strip()

    if not seed.startswith("s"):
        print("❌ 올바른 Seed가 아닙니다.")
        return

    wallet = Wallet.from_seed(seed)
    print(f"발신 주소: {wallet.classic_address}")

    with client:
        # 2. 현재 잔액 확인
        balance = get_account_balance(client, wallet.classic_address)
        print(f"현재 잔액: {balance:.6f} XRP")

        # 3. 송금 정보 입력
        destination = input("\n수신 주소 (r로 시작): ").strip()
        amount_xrp = float(input("송금할 XRP 수량 (예: 10): ").strip())

        destination_tag_input = input("Destination Tag (없으면 Enter): ").strip()
        destination_tag = int(destination_tag_input) if destination_tag_input else None

        # 4. 최종 확인
        print("\n=== 송금 정보 확인 ===")
        print(f"From: {wallet.classic_address}")
        print(f"To  : {destination}")
        if destination_tag:
            print(f"Tag : {destination_tag}")
        print(f"Amount: {amount_xrp} XRP")

        if not confirm_action("위 내용으로 XRP를 송금하시겠습니까?"):
            print("취소되었습니다.")
            return

        # 5. Payment 트랜잭션 생성
        payment = Payment(
            account=wallet.classic_address,
            destination=destination,
            amount=xrp_to_drops(amount_xrp),
            destination_tag=destination_tag,
        )

        print("\n트랜잭션 제출 중...")

        # 6. 서명 + 제출 + 결과 대기
        response = submit_and_wait(payment, client, wallet)

        # 7. 결과 출력
        print_transaction_result(response)


if __name__ == "__main__":
    main()