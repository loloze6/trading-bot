---
backtest: 010-02_rsi-below-midpoint-continues-down_1d
data: BTC, ETH, BNB as BTCUSD, ETHUSD, BNBUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8172 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1776 | above 0 | yes |
| Mean daily return | 0.0009305 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6722 | above 0 | yes |
| Calmar | 0.4667 | above 0.75 | no |
| Trades per bar | 0.2273 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night_run/backtests/010-02_rsi-below-midpoint-continues-down_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
