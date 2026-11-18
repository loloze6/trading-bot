---
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1035 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4507 | above 0 | no |
| Mean daily return | 1.184e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1239 | above 0 | no |
| Calmar | 0.05635 | above 0.75 | no |
| Trades per bar | 0.02887 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
