---
backtest: 002-03_price-cross-above-long-sma_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6758 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1062 | above 0 | yes |
| Mean daily return | 0.0005349 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4538 | above 0 | yes |
| Calmar | 0.3855 | above 0.75 | no |
| Trades per bar | 0.09957 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/full_data_run/backtests/002-03_price-cross-above-long-sma_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
