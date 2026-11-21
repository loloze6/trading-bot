---
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.064 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5094 | above 0 | yes |
| Mean daily return | 0.0007606 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.902 | above 0 | yes |
| Calmar | 1.236 | above 0.75 | yes |
| Trades per day | 0.132 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
