---
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2512 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3026 | above 0 | no |
| Mean daily return | 0.0003183 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1327 | above 0 | yes |
| Calmar | 0.008388 | above 0.75 | no |
| Trades per day | 0.6943 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/std_time_pilot_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
