---
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6918 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1376 | above 0 | yes |
| Mean daily return | 0.0002783 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5309 | above 0 | yes |
| Calmar | 0.5278 | above 0.75 | no |
| Trades per day | 0.05912 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
