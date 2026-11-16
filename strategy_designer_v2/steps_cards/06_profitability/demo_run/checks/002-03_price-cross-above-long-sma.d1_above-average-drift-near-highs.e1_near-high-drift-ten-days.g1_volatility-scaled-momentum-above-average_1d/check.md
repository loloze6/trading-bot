---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9217 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3676 | above 0 | yes |
| Mean daily return | 0.0005512 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.716 | above 0 | yes |
| Calmar | 0.7323 | above 0.75 | no |
| Trades per bar | 0.1643 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.g1_volatility-scaled-momentum-above-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
