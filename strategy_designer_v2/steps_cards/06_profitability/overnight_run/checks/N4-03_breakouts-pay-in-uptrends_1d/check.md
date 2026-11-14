---
backtest: N4-03_breakouts-pay-in-uptrends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.27 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2842 | above 0 | no |
| Mean daily return | 0.0001917 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.05248 | above 0 | no |
| Calmar | 0.06681 | above 0.75 | no |
| Trades per bar | 0.1917 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-03_breakouts-pay-in-uptrends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
