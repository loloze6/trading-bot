---
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9368 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3826 | above 0 | yes |
| Mean daily return | 0.0002913 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7897 | above 0 | yes |
| Calmar | 0.7462 | above 0.75 | no |
| Trades per day | 0.278 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
