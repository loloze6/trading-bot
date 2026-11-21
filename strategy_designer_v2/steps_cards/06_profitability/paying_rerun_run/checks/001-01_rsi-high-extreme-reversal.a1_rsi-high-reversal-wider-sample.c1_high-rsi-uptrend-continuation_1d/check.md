---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.065 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5105 | above 0 | yes |
| Mean daily return | 0.0007432 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9201 | above 0 | yes |
| Calmar | 1.103 | above 0.75 | yes |
| Trades per day | 0.1726 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
