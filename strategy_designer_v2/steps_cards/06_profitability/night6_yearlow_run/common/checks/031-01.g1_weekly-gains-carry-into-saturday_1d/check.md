---
backtest: 031-01.g1_weekly-gains-carry-into-saturday_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7417 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3335 | above 0 | no |
| Mean daily return, on days in a position | 0.001601 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.619 | above 0 | yes |
| Calmar | 0.5453 | above 0.75 | no |
| Trades per day | 0.05963 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.493 % |
| Yearly return | +6.8 % (over 10.59 years) |
| Days in a position | 12 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/common/backtests/031-01.g1_weekly-gains-carry-into-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
