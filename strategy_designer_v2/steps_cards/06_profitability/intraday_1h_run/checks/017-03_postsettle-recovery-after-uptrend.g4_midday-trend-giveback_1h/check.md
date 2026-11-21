---
backtest: 017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.728 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.282 | above 0 | no |
| Mean daily return | -0.0008909 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.921 | above 0 | no |
| Calmar | -0.3043 | above 0.75 | no |
| Trades per day | 1.489 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-03_postsettle-recovery-after-uptrend.g4_midday-trend-giveback_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
