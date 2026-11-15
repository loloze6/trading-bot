---
backtest: 002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8439 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2897 | above 0 | yes |
| Mean daily return | 0.0006776 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6572 | above 0 | yes |
| Calmar | 0.5433 | above 0.75 | no |
| Trades per bar | 0.1145 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b1_above-average-with-60-day-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
