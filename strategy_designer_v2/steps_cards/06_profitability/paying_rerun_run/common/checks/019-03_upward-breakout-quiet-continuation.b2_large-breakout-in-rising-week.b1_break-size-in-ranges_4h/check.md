---
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 4h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.693 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4076 | above 0 | yes |
| Mean daily return, on days in a position | 0.003549 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.534 | above 0 | yes |
| Calmar | 2.148 | above 0.75 | yes |
| Trades per day | 0.2097 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.936 % |
| Yearly return | +74.9 % (over 9.93 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
