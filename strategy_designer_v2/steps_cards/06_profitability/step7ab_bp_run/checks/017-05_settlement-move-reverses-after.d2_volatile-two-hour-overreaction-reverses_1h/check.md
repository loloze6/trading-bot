---
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.9002 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.454 | above 0 | no |
| Mean daily return | -0.0007428 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.05 | above 0 | no |
| Calmar | -0.2946 | above 0.75 | no |
| Trades per day | 2.713 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
