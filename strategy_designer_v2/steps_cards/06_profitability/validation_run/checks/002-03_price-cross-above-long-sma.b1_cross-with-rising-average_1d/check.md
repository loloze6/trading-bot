---
backtest: 002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6745 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.09284 | above 0 | yes |
| Mean daily return | 0.000489 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3758 | above 0 | yes |
| Calmar | 0.4105 | above 0.75 | no |
| Trades per bar | 0.03157 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b1_cross-with-rising-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
