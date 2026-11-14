---
backtest: N1-08_twenty-day-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3208 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2334 | above 0 | no |
| Mean daily return | 0.0007219 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2278 | above 0 | yes |
| Calmar | -0.08518 | above 0.75 | no |
| Trades per bar | 0.5075 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-08_twenty-day-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
