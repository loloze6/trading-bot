---
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.056 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5014 | above 0 | yes |
| Mean daily return | 0.0007548 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8937 | above 0 | yes |
| Calmar | 1.216 | above 0.75 | yes |
| Trades per bar | 0.132 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
