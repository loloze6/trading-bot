---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9977 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4435 | above 0 | yes |
| Mean daily return | 0.000695 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8014 | above 0 | yes |
| Calmar | 0.8558 | above 0.75 | yes |
| Trades per day | 0.09262 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
