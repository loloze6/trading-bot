---
backtest: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.465 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6102 | above 0 | no |
| Mean daily return, on days in a position | 0.0003608 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3564 | above 0 | yes |
| Calmar | 0.2015 | above 0.75 | no |
| Trades per day | 0.3384 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.923 % |
| Yearly return | +6.9 % (over 10.59 years) |
| Days in a position | 62 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/common/backtests/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
