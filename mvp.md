**MVP 목표**

주식 데이터를 주기적으로 수집해서 대시보드로 보여주고, 필요할 때 로컬 Codex 구독 환경으로 분석한 뒤 결과를 다시 저장/확인하는 구조입니다. Vercel은 자동 수집과 웹 대시보드만 담당하고, AI 분석은 OpenAI API가 아니라 **내 로컬 Codex**가 담당합니다.

**전체 구조**

```txt
cron-job.org / 로컬 cron
  -> Vercel API Route 호출
    -> 주식 API 호출
      -> Supabase/Neon DB 저장
        -> Next.js 대시보드 표시

로컬 Codex
  -> Cloud DB 조회
    -> 주식 데이터 분석
      -> 분석 결과 DB 저장
        -> 대시보드 표시
        -> 필요하면 Telegram/이메일 알림
```

**1단계: 데이터 저장소 준비**

Supabase 또는 Neon에 Postgres DB를 만듭니다.

필요한 테이블은 최소 이렇게 시작합니다.

```txt
stocks
- symbol
- name
- enabled

stock_prices
- id
- symbol
- price
- volume
- captured_at

stock_analysis
- id
- symbol
- summary
- signal
- risk_level
- created_at
```

처음에는 알림 테이블까지 만들지 않아도 됩니다.

**2단계: Next.js API Route 만들기**

파일 구조:

```txt
app/api/jobs/collect-stocks/route.ts
```

역할:

```txt
1. Authorization secret 확인
2. 수집 대상 종목 목록 조회
3. 외부 주식 API 호출
4. 가격/거래량 데이터를 DB에 저장
5. 성공/실패 결과 반환
```

배포 후 endpoint:

```txt
https://your-project.vercel.app/api/jobs/collect-stocks
```

**3단계: 외부 스케줄러 연결**

Vercel Hobby Cron은 하루 1회 제한이 있으므로, 1시간마다 돌리려면 외부 스케줄러를 씁니다.

추천:

```txt
cron-job.org
또는 Upstash QStash
또는 내 로컬 PC/NAS cron
```

호출 예:

```bash
curl -X POST \
  https://your-project.vercel.app/api/jobs/collect-stocks \
  -H "Authorization: Bearer $CRON_SECRET"
```

**4단계: 대시보드 만들기**

Next.js 페이지에서 DB를 조회해서 보여줍니다.

처음 화면은 이 정도면 충분합니다.

```txt
관심 종목 목록
현재가
최근 갱신 시간
24시간 변화율
간단한 차트
최근 AI 분석 요약
```

이 단계까지는 AI 없이도 동작해야 합니다.

**5단계: 로컬 Codex 분석 플로우 만들기**

로컬에 DB 조회/저장용 스크립트를 만듭니다.

예:

```bash
npm run stocks:export -- --symbol AAPL --days 30
npm run stocks:save-analysis
npm run stocks:notify
```

Codex에게는 이런 식으로 요청합니다.

```txt
최근 30일 AAPL, MSFT, NVDA 데이터를 조회해서
이상 움직임, 추세, 리스크를 요약하고
결과를 stock_analysis 테이블에 저장해줘.
```

즉 Codex가 직접 Cloud DB 데이터를 읽고 분석 결과를 다시 DB에 넣습니다.

**6단계: 알림 추가**

초기에는 Telegram Bot을 추천합니다.

알림은 두 방식 중 하나로 시작하면 됩니다.

```txt
서버 알림:
Vercel Function이 단순 조건을 판단해서 Telegram 발송

로컬 AI 알림:
Codex 분석 결과가 특정 조건이면 로컬 스크립트가 Telegram 발송
```

네 조건상 AI 판단 기반 알림은 로컬에서 하는 게 맞습니다.

**MVP에서 하지 않을 것**

처음에는 아래는 빼는 게 좋습니다.

```txt
Vercel 내부 SQLite
Vercel Pro Cron
OpenAI API 기반 자동 분석
복잡한 실시간 알림
모바일 앱 푸시
고빈도 분봉 수집
자동 매매
```

**최종 MVP 범위**

가장 현실적인 MVP는 이겁니다.

```txt
Vercel Hobby
+ Next.js 대시보드
+ Supabase/Neon Postgres
+ cron-job.org 1시간 주기 호출
+ 주식 API 데이터 저장
+ 로컬 Codex 분석
+ 분석 결과 DB 저장
+ 대시보드에서 분석 결과 확인
+ 선택적으로 Telegram 알림
```

이렇게 만들면 무료/저비용으로 시작하면서도, 나중에 필요하면 다음 단계로 확장할 수 있습니다.

```txt
외부 스케줄러 -> Vercel Pro Cron
로컬 Codex 분석 -> OpenAI API 자동 분석
Telegram 알림 -> PWA/모바일 푸시
단순 차트 -> 고급 백테스트/리포트
```
