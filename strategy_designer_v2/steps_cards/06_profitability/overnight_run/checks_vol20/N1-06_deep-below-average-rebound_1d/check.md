---
backtest: N1-06_deep-below-average-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5531 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01648 | above 0 | no |
| Mean daily return | 0.0003031 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3431 | above 0 | yes |
| Calmar | 0.2411 | above 0.75 | no |
| Trades per bar | 0.04853 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-06_deep-below-average-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
