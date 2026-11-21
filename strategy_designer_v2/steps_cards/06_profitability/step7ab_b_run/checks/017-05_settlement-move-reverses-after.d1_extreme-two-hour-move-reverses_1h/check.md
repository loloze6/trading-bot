---
backtest: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.7486 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.302 | above 0 | no |
| Mean daily return | -0.0007579 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.902 | above 0 | no |
| Calmar | -0.305 | above 0.75 | no |
| Trades per day | 1.446 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
