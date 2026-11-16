---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.861 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3068 | above 0 | yes |
| Mean daily return | 0.0004792 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6751 | above 0 | yes |
| Calmar | 0.6561 | above 0.75 | no |
| Trades per bar | 0.1593 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
