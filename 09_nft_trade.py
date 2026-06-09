"""
09. NFT 거래 (Sell Offer 생성 및 수락)

NFT를 판매하기 위한 오퍼를 만들고, 다른 계정이 수락하는 과정을 보여줍니다.

실제로는 두 개의 지갑(판매자, 구매자)이 필요합니다.
이 예제에서는 하나의 지갑으로 Sell Offer를 생성하는 부분까지 다룹니다.
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenCreateOffer
from xrpl.models.amounts import Amount
from xrpl.transaction import submit_and_wait
from xrpl.utils import xrp_to_drops
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== NFT Sell Offer 생성 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed (판매자): ").strip()
    wallet = Wallet.from_seed(seed)

    nft_id = input("판매할 NFT ID (NFTokenID): ").strip()
    price_xrp = float(input("판매 가격 (XRP): ").strip())

    print(f"\n판매자: {wallet.classic_address}")
    print(f"NFT ID: {nft_id}")
    print(f"가격: {price_xrp} XRP")

    if not confirm_action("위 내용으로 NFT Sell Offer를 생성하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        sell_offer = NFTokenCreateOffer(
            account=wallet.classic_address,
            nftoken_id=nft_id,
            amount=xrp_to_drops(price_xrp),
            flags=1,  # Sell offer
        )

        print("\nNFT Sell Offer 생성 중...")
        response = submit_and_wait(sell_offer, client, wallet)
        print_transaction_result(response)

        print("\n💡 구매자가 이 오퍼를 수락하려면 NFTokenAcceptOffer 트랜잭션을 사용합니다.")


if __name__ == "__main__":
    main()