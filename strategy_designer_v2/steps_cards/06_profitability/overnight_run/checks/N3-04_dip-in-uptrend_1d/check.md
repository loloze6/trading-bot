---
backtest: N3-04_dip-in-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7666 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2124 | above 0 | yes |
| Mean daily return | 0.0005773 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6106 | above 0 | yes |
| Calmar | 0.5209 | above 0.75 | no |
| Trades per bar | 0.09022 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-04_dip-in-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
