---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.024 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.47 | above 0 | yes |
| Mean daily return | 0.0007652 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.886 | above 0 | yes |
| Calmar | 0.8822 | above 0.75 | yes |
| Trades per bar | 0.24 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
