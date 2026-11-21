---
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9387 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8407 | above 0 | yes |
| Mean daily return | 0.0006614 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1995 | above 0 | yes |
| Calmar | 1.754 | above 0.75 | yes |
| Trades per day | 0.1366 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
