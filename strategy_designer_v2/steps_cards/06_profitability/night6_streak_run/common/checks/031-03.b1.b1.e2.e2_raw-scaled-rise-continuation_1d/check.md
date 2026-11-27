---
backtest: 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.004 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06067 | above 0 | no |
| Mean daily return, on days in a position | 0.005734 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8855 | above 0 | yes |
| Calmar | 0.6563 | above 0.75 | no |
| Trades per day | 0.02003 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.968 % |
| Yearly return | +18.4 % (over 10.59 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/common/backtests/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
