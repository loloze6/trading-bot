---
backtest: N2-01_weekday-of-coming-bar_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.478 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.08997 | above 0 | no |
| Mean daily return | 0.0002701 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.209 | above 0 | yes |
| Calmar | 0.1836 | above 0.75 | no |
| Trades per bar | 0.07649 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-01_weekday-of-coming-bar_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
