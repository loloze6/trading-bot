---
backtest: 013-03_breakout-above-high-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.08686 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4948 | above 0 | no |
| Mean daily return | 1.508e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.02714 | above 0 | no |
| Calmar | 0.051 | above 0.75 | no |
| Trades per bar | 0.009622 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar; Trades per bar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-03_breakout-above-high-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
