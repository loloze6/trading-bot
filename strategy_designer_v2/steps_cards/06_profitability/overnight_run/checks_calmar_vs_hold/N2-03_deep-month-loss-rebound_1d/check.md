---
backtest: N2-03_deep-month-loss-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3164 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2378 | above 0 | no |
| Mean daily return | 0.0005527 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2445 | above 0 | yes |
| Calmar | -0.007038 | above 0.16 | no |
| Trades per bar | 0.17 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-03_deep-month-loss-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
