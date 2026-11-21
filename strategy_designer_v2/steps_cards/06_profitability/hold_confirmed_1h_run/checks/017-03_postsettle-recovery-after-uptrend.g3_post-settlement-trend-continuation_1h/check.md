---
backtest: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.819 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.372 | above 0 | no |
| Mean daily return | -0.0005573 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.115 | above 0 | no |
| Calmar | -0.2317 | above 0.75 | no |
| Trades per day | 1.513 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
