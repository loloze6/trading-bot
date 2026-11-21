---
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.042 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.596 | above 0 | no |
| Mean daily return | -0.0007867 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.129 | above 0 | no |
| Calmar | -0.3006 | above 0.75 | no |
| Trades per day | 3.484 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
