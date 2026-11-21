---
backtest: 020-03_resistance-breakout-continues-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7423 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1881 | above 0 | yes |
| Mean daily return | 0.0008256 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5389 | above 0 | yes |
| Calmar | 0.4908 | above 0.75 | no |
| Trades per day | 0.1502 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
