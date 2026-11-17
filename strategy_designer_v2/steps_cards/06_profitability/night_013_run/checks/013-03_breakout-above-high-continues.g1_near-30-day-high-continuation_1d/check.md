---
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2851 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2691 | above 0 | no |
| Mean daily return | 7.904e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.08262 | above 0 | yes |
| Calmar | 0.106 | above 0.75 | no |
| Trades per bar | 0.1625 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_013_run/backtests/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
