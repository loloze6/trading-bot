---
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.162 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5895 | above 0 | no |
| Mean daily return | 0.004028 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.816 | above 0 | yes |
| Calmar | 11.77 | above 0.75 | yes |
| Trades per day | 0.1074 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night4_range_run/unseen_2016_2017/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
