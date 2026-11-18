---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.63 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.121 | above 0 | no |
| Mean daily return | 0.003849 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.204 | above 0 | yes |
| Calmar | 15.68 | above 0.75 | yes |
| Trades per bar | 0.235 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
