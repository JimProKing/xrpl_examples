"""
12. Ledger 데이터 조회

XRPL에서 다양한 데이터를 조회할 수 있습니다.

이 예제에서는:
- 특정 계정의 거래 내역 (AccountTx)
- 오더북 조회 (BookOffers)
"""

from xrpl.clients import WebsocketClient
from xrpl.models.requests import AccountTx, BookOffers
from xrpl.models.amounts import XRPAmount, IssuedCurrencyAmount
from common import get_client, TESTNET_URL


def main():
    print("=== Ledger 데이터 조회 예제 ===\n")

    client = get_client(TESTNET_URL)

    address = input("조회할 계정 주소: ").strip()

    with client:
        # 1. 계정 거래 내역 조회
        print("\n=== 1. 최근 거래 내역 (AccountTx) ===")
        try:
            tx_response = client.request(
                AccountTx(account=address, limit=5)
            )
            transactions = tx_response.result.get("transactions", [])

            if transactions:
                for tx in transactions:
                    tx_data = tx.get("tx", {})
                    print(f"- {tx_data.get('TransactionType')} | {tx_data.get('hash')[:20]}...")
            else:
                print("거래 내역이 없습니다.")
        except Exception as e:
            print(f"거래 내역 조회 실패: {e}")

        # 2. XRP / USD 오더북 조회 예시
        print("\n=== 2. 오더북 조회 (BookOffers) ===")
        try:
            taker_gets = XRPAmount("1000000")  # 1 XRP (drops)
            taker_pays = IssuedCurrencyAmount(
                currency="USD",
                issuer="rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh",  # 테스트넷 유명 발행자
                value="1"
            )

            book_response = client.request(
                BookOffers(
                    taker_gets=taker_gets,
                    taker_pays=taker_pays,
                    limit=3
                )
            )
            offers = book_response.result.get("offers", [])
            print(f"해당 오더북에 {len(offers)}개의 오퍼가 있습니다.")
        except Exception as e:
            print(f"오더북 조회 실패 (정상적일 수 있음): {e}")

    print("\n✅ 데이터 조회 완료!")


if __name__ == "__main__":
    main()