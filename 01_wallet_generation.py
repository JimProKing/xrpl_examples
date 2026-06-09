"""
01. 지갑(Wallet) 생성 및 관리

XRPL에서 가장 먼저 해야 할 일은 지갑을 만드는 것입니다.
지갑은 Seed(비밀키)와 Address(공개 주소)로 구성됩니다.

이 예제에서는:
- 새로운 지갑 생성
- Seed와 Address 확인
- Wallet 객체 사용법
"""

from xrpl.wallet import Wallet
from xrpl.clients import WebsocketClient
from common import get_client, TESTNET_URL


def main():
    print("=== XRPL 지갑 생성 예제 ===\n")

    # 1. 새로운 지갑 생성 (테스트넷용)
    # 실제 서비스에서는 사용자가 자신의 Seed를 안전하게 보관해야 합니다.
    wallet = Wallet.create()

    print("✅ 새로운 지갑이 생성되었습니다!")
    print(f"주소 (Address):     {wallet.classic_address}")
    print(f"시드 (Seed):        {wallet.seed}")
    print(f"공개키 (Public):    {wallet.public_key}")
    print(f"개인키 (Private):   {wallet.private_key}")

    print("\n📌 중요:")
    print("- Seed는 절대 다른 사람에게 알려주면 안 됩니다.")
    print("- Seed를 잃어버리면 계정에 접근할 수 없습니다.")
    print("- 테스트넷에서는 Faucet으로 무료 XRP를 받을 수 있습니다.")

    # 2. 기존 Seed로 지갑 복원하는 방법
    print("\n=== 기존 Seed로 지갑 복원하기 ===")
    seed = wallet.seed  # 위에서 생성한 seed 사용
    restored_wallet = Wallet.from_seed(seed)

    print(f"복원된 주소: {restored_wallet.classic_address}")
    print("같은 주소가 나오는지 확인하세요!")

    # 3. 테스트넷에 연결해서 지갑 정보 확인 (선택)
    print("\n=== 테스트넷 연결 테스트 ===")
    client = get_client(TESTNET_URL)

    with client:
        print(f"테스트넷에 성공적으로 연결되었습니다.")
        print(f"현재 사용 중인 노드: {TESTNET_URL}")

    print("\n💡 다음 단계 추천:")
    print("1. 생성된 Seed와 Address를 메모하세요.")
    print("2. https://xrpl.org/resources/dev-tools/xrp-faucets 에서 테스트 XRP 받기")
    print("3. 02_account_info.py 로 잔액 확인해보기")


if __name__ == "__main__":
    main()