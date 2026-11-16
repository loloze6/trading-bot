---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.06575 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6199 | above 0 | no |
| Mean daily return | -2.138e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2088 | above 0 | no |
| Calmar | -0.04222 | above 0.75 | no |
| Trades per bar | 0.1102 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
