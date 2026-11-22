---
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8542 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2467 | above 0 | yes |
| Mean daily return | 0.0007566 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7365 | above 0 | yes |
| Calmar | 0.9189 | above 0.75 | yes |
| Trades per day | 0.1754 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
