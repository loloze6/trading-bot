---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -3.21 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.763 | above 0 | no |
| Mean daily return | -0.001761 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -3.425 | above 0 | no |
| Calmar | -0.4871 | above 0.75 | no |
| Trades per day | 3.804 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
