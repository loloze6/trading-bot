---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.03 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.0707 | above 0 | yes |
| Mean daily return, on days in a position | 0.002037 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9434 | above 0 | yes |
| Calmar | 0.7034 | above 0.75 | no |
| Trades per day | 0.08253 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.504 % |
| Yearly return | +9.9 % (over 9.92 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/common/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
