---
backtest: N1-02_above-rising-long-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5424 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02724 | above 0 | no |
| Mean daily return | 0.0009214 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2104 | above 0 | yes |
| Calmar | 0.182 | above 0.1811 | yes |
| Trades per bar | 0.08687 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-02_above-rising-long-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
