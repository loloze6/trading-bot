---
backtest: 011-01_weekend-rise-reverses-monday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.01342 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5676 | above 0 | no |
| Mean daily return | -3.477e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1374 | above 0 | no |
| Calmar | -0.02905 | above 0.75 | no |
| Trades per bar | 0.06003 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
