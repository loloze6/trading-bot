---
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1h bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.641 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5411 | above 0 | yes |
| Mean daily return, on days in a position | 0.002383 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.477 | above 0 | yes |
| Calmar | 1.621 | above 0.75 | yes |
| Trades per day | 0.2488 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.806 % |
| Yearly return | +66.0 % (over 10.59 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e1_monthly-rise-weekly-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
