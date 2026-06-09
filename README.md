# XRPL Python 예제 모음

안녕하세요.

XRPL(XRP Ledger)을 처음 공부하면서, 공식 문서를 보면서 따라 해보려고 했는데 예제가 너무 부족하고 영어로 되어 있어서 직접 하나씩 만들어보게 됐습니다.

이 저장소는 XRPL에서 자주 쓰이는 기능들을 **Python**으로 실습할 수 있게 정리한 예제 모음입니다. 각 기능별로 파일을 분리해서, 필요한 부분만 골라서 볼 수 있게 했어요.

초보자도 README만 보고 따라할 수 있도록 최대한 자세히 적었습니다.

## 목차

- [시작하기](#시작하기)
- [주의사항](#주의사항)
- [예제 목록](#예제-목록)
- [실행 방법](#실행-방법)
- [학습 추천 순서](#학습-추천-순서)
- [테스트넷 vs 메인넷](#테스트넷-vs-메인넷)
- [자주 묻는 질문](#자주-묻는-질문)

## 시작하기

### 설치

```bash
cd xrpl_examples
pip install -r requirements.txt
```

### 테스트넷 계정 만들기

1. [XRP Testnet Faucet](https://xrpl.org/resources/dev-tools/xrp-faucets) 사이트에 접속하세요.
2. **Generate Testnet Credentials** 버튼을 누릅니다.
3. 나온 **Seed**와 **Address**를 잘 메모해두세요.

> ⚠️ Seed는 절대 다른 사람에게 알려주거나, GitHub에 올리면 안 됩니다.

## 주의사항

- 이 예제들은 **기본적으로 테스트넷**에서 동작합니다.
- 메인넷에서 실행하려면 각 파일 상단의 `CLIENT_URL`을 메인넷 주소로 바꿔야 합니다.
- 메인넷에서 실험할 때는 **반드시 소액**으로만 테스트하세요.
- Seed는 절대 코드 안에 하드코딩하지 마세요.

## 예제 목록

| 파일 | 설명 | 난이도 |
|------|------|--------|
| `01_wallet_generation.py` | 지갑 생성하고 Seed, Address 확인하기 | 초급 |
| `02_account_info.py` | 계정 잔액, Sequence, Flags 등 조회 | 초급 |
| `03_send_xrp.py` | XRP 직접 보내기 | 초급 |
| `04_trustline.py` | Issued Currency를 받기 위한 Trust Line 만들기 | 중급 |
| `05_send_issued_currency.py` | Trust Line으로 토큰(USD 등) 보내기 | 중급 |
| `06_dex_offer.py` | DEX에 매수/매도 주문 넣기 | 중급 |
| `07_escrow.py` | 시간이나 조건으로 XRP 잠가두기 (Escrow) | 중상 |
| `08_nft_mint.py` | NFT 발행하기 | 중상 |
| `09_nft_trade.py` | NFT 판매 오퍼 만들기 | 중상 |
| `10_checks.py` | 수표(Checks) 기능 사용하기 | 중상 |
| `11_account_settings.py` | 계정에 RequireDestTag 같은 설정 걸기 | 중급 |
| `12_get_ledger_data.py` | 거래 내역, 오더북 등 데이터 조회하기 | 중급 |

## 실행 방법

각 파일은 독립적으로 실행할 수 있습니다.

예시:

```bash
python 01_wallet_generation.py
python 03_send_xrp.py
```

실행하면 대부분 아래 순서로 동작합니다:
1. 테스트넷에 연결
2. 지갑 정보 로드
3. 트랜잭션 준비 및 서명
4. 결과 출력 + Explorer 링크 보여주기

## 학습 추천 순서

1. `01_wallet_generation.py` → 지갑이 뭔지부터 이해
2. `02_account_info.py` → 내 계정이 어떤 상태인지 보는 법
3. `03_send_xrp.py` → 가장 기본적인 송금
4. `04_trustline.py` + `05_send_issued_currency.py` → 토큰 개념
5. 그 다음부터 관심 있는 기능 순으로 보면 됩니다.

## 테스트넷 vs 메인넷

### 테스트넷 (강력 추천)
- 주소: `wss://s.altnet.rippletest.net:51233`
- Faucet으로 무료 XRP 받을 수 있음
- 실수해도 복구 가능

### 메인넷
- 주소: `wss://xrplcluster.com/`
- 실제 돈이 움직임
- 소액으로만 테스트하세요

각 파일 상단에 `CLIENT_URL` 변수가 있으니, 이 부분만 바꾸면 네트워크를 전환할 수 있습니다.

## 자주 묻는 질문

**Q. Seed가 뭔가요?**  
A. 계정의 비밀키입니다. 이걸 알아야 계정에 접근할 수 있어요. 절대 유출되면 안 됩니다.

**Q. 테스트넷 XRP는 어디서 받나요?**  
A. https://xrpl.org/resources/dev-tools/xrp-faucets 여기서 받을 수 있습니다.

**Q. 메인넷에서 바로 써도 되나요?**  
A. 추천하지 않습니다. 테스트넷에서 충분히 익힌 후에 소액으로 테스트하세요.

**Q. 이 코드로 실제 서비스를 만들어도 되나요?**  
A. 이건 학습용 예제입니다. 실제 서비스를 만들 때는 에러 처리, 보안, 재시도 로직 등을 더 신경 써야 합니다.

---

이 저장소가 XRPL을 처음 접하는 분들에게 조금이라도 도움이 되었으면 좋겠습니다.

궁금한 점이나 개선 제안이 있으면 언제든 이슈나 PR로 말씀해주세요.

행복한 XRPL 개발 되세요! 🚀

---

*마지막 업데이트: 2026년*