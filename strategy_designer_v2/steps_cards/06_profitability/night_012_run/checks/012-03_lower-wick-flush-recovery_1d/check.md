---
backtest: 012-03_lower-wick-flush-recovery_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08405 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6382 | above 0 | no |
| Mean daily return | -6.766e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2143 | above 0 | no |
| Calmar | -0.0368 | above 0.75 | no |
| Trades per bar | 0.01044 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_012_run/backtests/012-03_lower-wick-flush-recovery_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
