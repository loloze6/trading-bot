---
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.524 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4241 | above 0 | yes |
| Mean daily return, on days in a position | 0.001945 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.354 | above 0 | yes |
| Calmar | 1.547 | above 0.75 | yes |
| Trades per day | 0.6503 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.842 % |
| Yearly return | +60.8 % (over 10.59 years) |
| Days in a position | 76 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
