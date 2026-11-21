---
backtest: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.02485 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5293 | above 0 | no |
| Mean daily return | 2.509e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.15 | above 0 | no |
| Calmar | -0.07753 | above 0.75 | no |
| Trades per day | 0.1419 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
