---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.522 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.424 | above 0 | yes |
| Mean daily return | 0.001057 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6555 | above 0 | yes |
| Calmar | 3.856 | above 0.75 | yes |
| Trades per bar | 0.1532 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
