---
backtest: 029-03_close-below-breakout-bar-low_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4997 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05443 | above 0 | no |
| Mean daily return | 5.199e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.349 | above 0 | yes |
| Calmar | 0.2059 | above 0.75 | no |
| Trades per day | 0.004965 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-03_close-below-breakout-bar-low_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
