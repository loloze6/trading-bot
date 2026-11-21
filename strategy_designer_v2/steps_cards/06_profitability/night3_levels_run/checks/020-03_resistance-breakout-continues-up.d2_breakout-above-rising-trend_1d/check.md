---
backtest: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.066 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5116 | above 0 | yes |
| Mean daily return | 0.0004368 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8965 | above 0 | yes |
| Calmar | 0.8529 | above 0.75 | yes |
| Trades per day | 0.06083 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
