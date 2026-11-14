---
backtest: N1-04_rebound-after-large-drop_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7826 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2319 | above 0 | yes |
| Mean daily return | 0.0004288 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6111 | above 0 | yes |
| Calmar | 0.8371 | above 0.75 | yes |
| Trades per bar | 0.2229 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-04_rebound-after-large-drop_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
