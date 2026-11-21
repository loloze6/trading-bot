---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8923 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3381 | above 0 | yes |
| Mean daily return | 0.0006669 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7455 | above 0 | yes |
| Calmar | 0.7815 | above 0.75 | yes |
| Trades per day | 0.1226 | at least 0.01 | yes |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
