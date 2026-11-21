---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9174 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3098 | above 0 | yes |
| Mean daily return | 0.0006343 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8088 | above 0 | yes |
| Calmar | 0.5371 | above 0.75 | no |
| Trades per day | 0.2158 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
