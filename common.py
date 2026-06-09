"""
XRPL 예제 공통 유틸리티
모든 예제에서 재사용할 수 있는 헬퍼 함수들
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountInfo
from xrpl.utils import xrp_to_drops

# ==================== 네트워크 설정 ====================
# 테스트넷 (기본 추천 - 안전)
TESTNET_URL = "wss://s.altnet.rippletest.net:51233"

# 메인넷 (실제 자산 사용 - 주의!)
MAINNET_URL = "wss://xrplcluster.com/"

# 현재 사용할 네트워크 (필요시 변경)
DEFAULT_CLIENT_URL = TESTNET_URL


def get_client(url: str = None) -> WebsocketClient:
    """XRPL WebSocket 클라이언트 반환"""
    if url is None:
        url = DEFAULT_CLIENT_URL
    return WebsocketClient(url)


def get_account_balance(client: WebsocketClient, address: str) -> float:
    """계정의 XRP 잔액 조회 (XRP 단위)"""
    try:
        response = client.request(AccountInfo(account=address))
        balance_drops = int(response.result["account_data"]["Balance"])
        return balance_drops / 1_000_000
    except Exception as e:
        print(f"잔액 조회 실패: {e}")
        return 0.0


def print_transaction_result(response):
    """트랜잭션 결과 예쁘게 출력"""
    result = response.result
    tx_hash = result.get("hash", "N/A")
    engine_result = result.get("engine_result", "N/A")
    message = result.get("engine_result_message", "")

    print(f"\n=== 트랜잭션 결과 ===")
    print(f"해시: {tx_hash}")
    print(f"상태: {engine_result}")
    print(f"메시지: {message}")

    if engine_result == "tesSUCCESS":
        print("✅ 성공!")
        print(f"Explorer: https://livenet.xrpl.org/transactions/{tx_hash}")
    else:
        print("❌ 실패 또는 부분 실패")

    return result


def confirm_action(message: str) -> bool:
    """사용자에게 최종 확인 요청"""
    print(f"\n⚠️  {message}")
    answer = input("정말 실행하시겠습니까? (YES 입력): ").strip().upper()
    return answer == "YES"