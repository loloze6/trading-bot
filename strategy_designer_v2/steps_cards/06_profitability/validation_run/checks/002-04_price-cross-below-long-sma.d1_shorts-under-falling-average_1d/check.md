---
backtest: 002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1577 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7234 | above 0 | no |
| Mean daily return | -9.693e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4039 | above 0 | no |
| Calmar | -0.08977 | above 0.75 | no |
| Trades per bar | 0.03097 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/backtests/002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
