---
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.438 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3633 | above 0 | yes |
| Mean daily return, on days in a position | 0.003884 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.292 | above 0 | yes |
| Calmar | 1.281 | above 0.75 | yes |
| Trades per day | 0.06036 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.739 % |
| Yearly return | +52.7 % (over 10.59 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/common/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
