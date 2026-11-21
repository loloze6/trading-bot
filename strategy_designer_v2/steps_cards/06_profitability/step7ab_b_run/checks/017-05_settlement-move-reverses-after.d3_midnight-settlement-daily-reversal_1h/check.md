---
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2069 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3468 | above 0 | no |
| Mean daily return | 0.0001808 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.008573 | above 0 | yes |
| Calmar | 0.02592 | above 0.75 | no |
| Trades per day | 1.592 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
