---
backtest: N4-04_dip-rebound-spans-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7698 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2157 | above 0 | yes |
| Mean daily return | 0.0005879 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6182 | above 0 | yes |
| Calmar | 0.5393 | above 0.16 | yes |
| Trades per bar | 0.07983 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-04_dip-rebound-spans-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
