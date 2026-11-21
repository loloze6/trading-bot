---
backtest: 022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6823 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1281 | above 0 | yes |
| Mean daily return | 0.0008786 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.51 | above 0 | yes |
| Calmar | 0.4176 | above 0.75 | no |
| Trades per day | 0.2934 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
