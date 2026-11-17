---
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1599 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3943 | above 0 | no |
| Mean daily return | 5.62e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.05523 | above 0 | yes |
| Calmar | 0.06144 | above 0.75 | no |
| Trades per bar | 0.1185 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
