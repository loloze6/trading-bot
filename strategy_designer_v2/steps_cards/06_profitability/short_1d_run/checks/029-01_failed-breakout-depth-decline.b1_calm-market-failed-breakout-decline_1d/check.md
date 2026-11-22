---
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4576 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.012 | above 0 | no |
| Mean daily return | -0.0002615 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5476 | above 0 | no |
| Calmar | -0.1682 | above 0.75 | no |
| Trades per day | 0.06996 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
