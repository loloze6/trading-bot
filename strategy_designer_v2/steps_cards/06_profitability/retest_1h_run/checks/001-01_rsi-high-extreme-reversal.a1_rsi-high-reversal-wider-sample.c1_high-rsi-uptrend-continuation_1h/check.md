---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -2.049 | above 0 | no |
| Sharpe minus holding's Sharpe | -2.603 | above 0 | no |
| Mean daily return | -0.001451 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -2.306 | above 0 | no |
| Calmar | -0.4353 | above 0.75 | no |
| Trades per day | 5.599 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_1h_run/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
