---
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5015 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.055 | above 0 | no |
| Mean daily return | -0.0003377 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6824 | above 0 | no |
| Calmar | -0.1864 | above 0.75 | no |
| Trades per day | 3.87 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
