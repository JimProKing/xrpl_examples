"""
08. NFT 민팅 (Non-Fungible Token)

XRPL에서 NFT를 발행하는 방법입니다.

주요 파라미터:
- URI: NFT의 메타데이터 위치 (보통 IPFS)
- Flags: 1 = burnable, 2 = onlyXRP, 8 = transferable 등
- TransferFee: 2차 판매 시 수수료 (0~50000 = 0~50%)
"""

from xrpl.clients import WebsocketClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenMint
from xrpl.transaction import submit_and_wait
from common import get_client, TESTNET_URL, print_transaction_result, confirm_action


def main():
    print("=== NFT 민팅 예제 ===\n")

    client = get_client(TESTNET_URL)

    seed = input("Seed: ").strip()
    wallet = Wallet.from_seed(seed)

    uri = input("NFT URI (예: ipfs://... 또는 https://...): ").strip()
    flags = int(input("Flags (기본 8=transferable): ") or "8")
    transfer_fee = int(input("Transfer Fee (0~50000, 기본 0): ") or "0")

    print(f"\n발행자: {wallet.classic_address}")
    print(f"URI: {uri}")
    print(f"Flags: {flags}")
    print(f"TransferFee: {transfer_fee}")

    if not confirm_action("위 내용으로 NFT를 민팅하시겠습니까?"):
        print("취소되었습니다.")
        return

    with client:
        nft_mint = NFTokenMint(
            account=wallet.classic_address,
            uri=uri.encode("utf-8").hex(),   # XRPL은 hex 인코딩 필요
            flags=flags,
            transfer_fee=transfer_fee,
            nftoken_taxon=0,                 # 분류용 숫자 (0부터 시작 추천)
        )

        print("\nNFT 민팅 중...")
        response = submit_and_wait(nft_mint, client, wallet)
        print_transaction_result(response)


if __name__ == "__main__":
    main()