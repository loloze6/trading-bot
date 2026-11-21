---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6751 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.121 | above 0 | yes |
| Mean daily return | 0.001247 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5319 | above 0 | yes |
| Calmar | 0.3533 | above 0.75 | no |
| Trades per day | 0.03709 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
