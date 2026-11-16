---
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7621 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2079 | above 0 | yes |
| Mean daily return | 0.0002085 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6522 | above 0 | yes |
| Calmar | 0.3573 | above 0.75 | no |
| Trades per bar | 0.07555 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
