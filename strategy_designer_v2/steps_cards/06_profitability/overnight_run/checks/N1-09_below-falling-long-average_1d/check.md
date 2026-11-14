---
backtest: N1-09_below-falling-long-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2553 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.821 | above 0 | no |
| Mean daily return | -0.0004056 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5172 | above 0 | no |
| Calmar | -0.2846 | above 0.75 | no |
| Trades per bar | 0.07613 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-09_below-falling-long-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
