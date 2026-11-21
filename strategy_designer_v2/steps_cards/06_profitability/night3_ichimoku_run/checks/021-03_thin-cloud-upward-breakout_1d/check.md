---
backtest: 021-03_thin-cloud-upward-breakout_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9159 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3502 | above 0 | yes |
| Mean daily return | 0.0004404 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.6863 | above 0 | yes |
| Calmar | 0.6809 | above 0.75 | no |
| Trades per day | 0.01683 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
