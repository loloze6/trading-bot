---
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.44 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.994 | above 0 | no |
| Mean daily return | -0.001114 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.519 | above 0 | no |
| Calmar | -0.3726 | above 0.75 | no |
| Trades per day | 3.321 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
