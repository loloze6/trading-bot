---
backtest: 002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8704 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3007 | above 0 | yes |
| Mean daily return | 0.0005677 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6885 | above 0 | yes |
| Calmar | 0.7402 | above 0.75 | no |
| Trades per bar | 0.1201 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.b2_above-average-with-momentum_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
