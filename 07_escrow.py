"""
07. Escrow (에스크로) 생성 및 완료

Escrow는 특정 시간이나 조건이 충족될 때까지 XRP를 잠그는 기능입니다.

이 예제에서는:
1. 1시간 후에 완료 가능한 Escrow 생성
2. Escrow 완료 (Finish)

실제 사용 시에는 FinishEscrow를 별도 계정이나 조건으로 수행할 수 있습니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import EscrowCreate, EscrowFinish
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops
from xrpl.ledger import get_latest_validated_ledger_sequence
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action
import time


def main():
    print("=== Escrow 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed: ").strip()
    wallet = Wallet.from_seed(seed)

    amount_xrp = float(input("Escrow에 잠글 XRP 수량: ").strip())

    # 1시간 후 (3600초) 완료 가능하도록 설정
    finish_after_seconds = 3600
    print(f"\n{finish_after_seconds}초 (1시간) 후에 완료 가능하도록 Escrow를 생성합니다.")

    if not confirm_action("Escrow를 생성하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        # 현재 Ledger Sequence 가져오기
        ledger_response = client.request({"command": "ledger_current"})
        current_ledger = ledger_response.result["ledger_current_index"]

        # EscrowCreate
        escrow_create = EscrowCreate(
            account=wallet.classic_address,
            amount=xrp_to_drops(amount_xrp),
            destination=wallet.classic_address,  # 자신에게 보내는 예시
            finish_after=current_ledger + 10,    # 대략적인 시간 조건 (실제로는 시간 기반)
        )

        print("\nEscrow 생성 중...")
        create_response = submit_and_wait(escrow_create, client, wallet)
        result = print_transaction_result(create_response)

        # Escrow Sequence 추출 (실제로는 더 정교하게 처리해야 함)
        if "tesSUCCESS" in str(result):
            print("\n✅ Escrow가 생성되었습니다.")
            print("Escrow Sequence는 트랜잭션 메타데이터에서 확인할 수 있습니다.")
            print("실제 FinishEscrow를 하려면 Escrow의 Sequence 번호가 필요합니다.")

            # 간단한 예시로 바로 Finish 시도 (테스트용)
            escrow_sequence = int(input("\n생성된 Escrow의 Sequence 번호를 입력하세요 (메타데이터 확인 필요): "))

            if confirm_action("이 Escrow를 지금 완료(Finish)하시겠습니까?"):
                escrow_finish = EscrowFinish(
                    account=wallet.classic_address,
                    owner=wallet.classic_address,
                    offer_sequence=escrow_sequence,
                )
                print("\nEscrow 완료 시도 중...")
                finish_response = submit_and_wait(escrow_finish, client, wallet)
                print_transaction_result(finish_response)


if __name__ == "__main__":
    main()