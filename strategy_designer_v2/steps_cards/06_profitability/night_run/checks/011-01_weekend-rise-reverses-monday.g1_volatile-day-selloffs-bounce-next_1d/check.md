---
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7317 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1775 | above 0 | yes |
| Mean daily return | 0.0004504 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5678 | above 0 | yes |
| Calmar | 0.5963 | above 0.75 | no |
| Trades per bar | 0.2152 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
