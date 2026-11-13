---
backtest: N7-01_drift-only-near-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9597 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4056 | above 0 | yes |
| Mean daily return | 0.001479 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7652 | above 0 | yes |
| Calmar | 0.685 | above 0.16 | yes |
| Trades per bar | 0.1554 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests/N7-01_drift-only-near-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
