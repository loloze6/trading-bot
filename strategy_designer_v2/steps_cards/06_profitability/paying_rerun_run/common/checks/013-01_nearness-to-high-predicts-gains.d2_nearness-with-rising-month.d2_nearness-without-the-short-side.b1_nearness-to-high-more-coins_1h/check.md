---
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.376 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2974 | above 0 | yes |
| Mean daily return, on days in a position | 0.001777 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.262 | above 0 | yes |
| Calmar | 1.383 | above 0.75 | yes |
| Trades per day | 0.8441 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.332 % |
| Yearly return | +37.4 % (over 9.92 years) |
| Days in a position | 54 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
