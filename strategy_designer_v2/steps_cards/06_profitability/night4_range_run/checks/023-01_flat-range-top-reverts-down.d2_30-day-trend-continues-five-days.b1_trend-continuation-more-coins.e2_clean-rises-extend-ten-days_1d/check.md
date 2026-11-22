---
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.033 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4258 | above 0 | yes |
| Mean daily return | 0.000791 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8586 | above 0 | yes |
| Calmar | 0.9222 | above 0.75 | yes |
| Trades per day | 0.06509 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
