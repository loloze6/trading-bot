---
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9031 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3489 | above 0 | yes |
| Mean daily return | 0.0006466 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6898 | above 0 | yes |
| Calmar | 0.6732 | above 0.75 | no |
| Trades per day | 0.1115 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
