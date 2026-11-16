---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9299 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3757 | above 0 | yes |
| Mean daily return | 0.0003985 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7466 | above 0 | yes |
| Calmar | 0.5825 | above 0.75 | no |
| Trades per bar | 0.1598 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
