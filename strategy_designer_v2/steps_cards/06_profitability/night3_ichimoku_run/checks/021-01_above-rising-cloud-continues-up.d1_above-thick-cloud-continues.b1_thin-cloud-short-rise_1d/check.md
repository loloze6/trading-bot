---
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9363 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3822 | above 0 | yes |
| Mean daily return | 0.0004593 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7067 | above 0 | yes |
| Calmar | 0.853 | above 0.75 | yes |
| Trades per day | 0.05764 | at least 0.01 | yes |

- Decided by: failed: Mean daily return
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
