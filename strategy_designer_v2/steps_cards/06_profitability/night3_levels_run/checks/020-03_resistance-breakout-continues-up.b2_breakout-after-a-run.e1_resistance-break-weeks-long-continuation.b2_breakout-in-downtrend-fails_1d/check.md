---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3661 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9203 | above 0 | no |
| Mean daily return | -0.0002506 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4976 | above 0 | no |
| Calmar | -0.1499 | above 0.75 | no |
| Trades per day | 0.04371 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
