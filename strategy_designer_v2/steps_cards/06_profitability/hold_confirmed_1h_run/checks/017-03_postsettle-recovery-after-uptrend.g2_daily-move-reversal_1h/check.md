---
backtest: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4548 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.09891 | above 0 | no |
| Mean daily return | 0.0004814 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3177 | above 0 | yes |
| Calmar | 0.178 | above 0.75 | no |
| Trades per day | 1.088 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
