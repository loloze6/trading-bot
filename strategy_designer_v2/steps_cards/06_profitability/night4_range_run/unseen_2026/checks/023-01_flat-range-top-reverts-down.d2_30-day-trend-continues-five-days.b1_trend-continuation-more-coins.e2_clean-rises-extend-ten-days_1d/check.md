---
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.956 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8896 | above 0 | yes |
| Mean daily return | 0.0005789 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2151 | above 0 | yes |
| Calmar | 1.927 | above 0.75 | yes |
| Trades per day | 0.06296 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
