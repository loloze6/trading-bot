---
backtest: 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.882 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.06284 | above 0 | no |
| Mean daily return, on days in a position | 0.00266 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6684 | above 0 | yes |
| Calmar | 0.9877 | above 0.75 | yes |
| Trades per day | 0.01279 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.149 % |
| Yearly return | +2.5 % (over 10.59 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/common/backtests/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
