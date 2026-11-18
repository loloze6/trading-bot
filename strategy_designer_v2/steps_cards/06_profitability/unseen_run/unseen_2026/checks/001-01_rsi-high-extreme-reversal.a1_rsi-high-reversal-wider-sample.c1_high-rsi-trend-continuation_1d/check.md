---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.259 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.161 | above 0 | yes |
| Mean daily return | 0.000925 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1457 | above 0 | yes |
| Calmar | 2.263 | above 0.75 | yes |
| Trades per bar | 0.2201 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/unseen_run/unseen_2026/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
