---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9276 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3735 | above 0 | yes |
| Mean daily return | 0.0008522 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7389 | above 0 | yes |
| Calmar | 0.8579 | above 0.75 | yes |
| Trades per day | 0.0545 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/hold2_rerun/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
