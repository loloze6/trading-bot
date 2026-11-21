---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9104 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3562 | above 0 | yes |
| Mean daily return | 0.00086 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7248 | above 0 | yes |
| Calmar | 0.7857 | above 0.75 | yes |
| Trades per day | 0.05027 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold_paying_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
