---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9487 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3829 | above 0 | yes |
| Mean daily return | 0.0005609 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7835 | above 0 | yes |
| Calmar | 0.9168 | above 0.75 | yes |
| Trades per bar | 0.1584 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
