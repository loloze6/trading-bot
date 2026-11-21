---
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.031 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4767 | above 0 | yes |
| Mean daily return | 0.0009092 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8704 | above 0 | yes |
| Calmar | 0.9654 | above 0.75 | yes |
| Trades per day | 0.1455 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
