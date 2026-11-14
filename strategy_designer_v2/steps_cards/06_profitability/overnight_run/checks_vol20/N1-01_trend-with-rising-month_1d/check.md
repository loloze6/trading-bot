---
backtest: N1-01_trend-with-rising-month_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6948 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.146 | above 0 | yes |
| Mean daily return | 0.0003807 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5165 | above 0 | yes |
| Calmar | 0.6566 | above 0.75 | no |
| Trades per bar | 0.1292 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-01_trend-with-rising-month_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
