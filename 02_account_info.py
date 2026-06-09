"""
02. 계정 정보 조회 (Account Info)

계정의 잔액, Sequence 번호, 설정 플래그 등을 조회합니다.
모든 트랜잭션을 보내기 전에 계정 상태를 확인하는 것이 좋습니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.models.requests import AccountInfo, AccountLines, AccountObjects
from xrpl.utils import drops_to_xrp
from common import get_client, TESTNET_URL


def main():
    print("=== XRPL 계정 정보 조회 예제 ===\n")

    # 테스트넷 계정 주소 입력 (Faucet으로 받은 주소 사용)
    address = input("조회할 XRPL 주소 (r로 시작)를 입력하세요: ").strip()

    if not address.startswith("r"):
        print("❌ 올바른 XRPL 주소가 아닙니다. (r로 시작해야 합니다)")
        return

    client = get_client(TESTNET_URL)

    with client:
        print(f"\n📡 {TESTNET_URL} 에 연결 중...")

        # 1. 기본 계정 정보 조회
        print("\n=== 1. 기본 계정 정보 (AccountInfo) ===")
        try:
            response = client.request(AccountInfo(account=address))
            account_data = response.result["account_data"]

            balance_drops = int(account_data["Balance"])
            balance_xrp = drops_to_xrp(balance_drops)
            sequence = account_data["Sequence"]
            owner_count = account_data.get("OwnerCount", 0)
            flags = account_data.get("Flags", 0)

            print(f"주소: {address}")
            print(f"잔액: {balance_xrp:.6f} XRP ({balance_drops} drops)")
            print(f"Sequence: {sequence}")
            print(f"OwnerCount (보유 중인 객체 수): {owner_count}")
            print(f"Flags: {flags}")

        except Exception as e:
            print(f"❌ 계정 정보 조회 실패: {e}")
            print("   - 주소가 존재하지 않거나, 아직 활성화되지 않았을 수 있습니다.")
            print("   - 테스트넷 Faucet에서 먼저 XRP를 받아보세요.")
            return

        # 2. Trust Line 조회 (발행 토큰 관계)
        print("\n=== 2. Trust Line 조회 (AccountLines) ===")
        try:
            lines_response = client.request(AccountLines(account=address))
            lines = lines_response.result.get("lines", [])

            if lines:
                print(f"총 {len(lines)}개의 Trust Line이 있습니다:")
                for line in lines:
                    print(f"  - {line['currency']} @ {line['account']}")
                    print(f"    잔액: {line['balance']}, 한도: {line['limit']}")
            else:
                print("Trust Line이 없습니다. (아직 발행 토큰을 받지 않음)")
        except Exception as e:
            print(f"Trust Line 조회 실패: {e}")

        # 3. Account Objects 조회 (Escrow, Check, Offer 등)
        print("\n=== 3. 계정이 소유한 객체 조회 (AccountObjects) ===")
        try:
            objects_response = client.request(AccountObjects(account=address))
            objects = objects_response.result.get("account_objects", [])

            if objects:
                print(f"총 {len(objects)}개의 객체가 있습니다:")
                for obj in objects:
                    obj_type = obj.get("LedgerEntryType", "Unknown")
                    print(f"  - {obj_type}")
            else:
                print("현재 소유한 객체(Escrow, Offer, Check 등)가 없습니다.")
        except Exception as e:
            print(f"AccountObjects 조회 실패: {e}")

    print("\n✅ 계정 정보 조회 완료!")
    print("💡 다음 추천: 03_send_xrp.py 로 XRP를 보내 보세요.")


if __name__ == "__main__":
    main()