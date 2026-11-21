---
backtest: 021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2449 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3208 | above 0 | no |
| Mean daily return | 1.049e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.09863 | above 0 | yes |
| Calmar | 0.1046 | above 0.75 | no |
| Trades per day | 0.001264 | at least 0.01 | no |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar; Trades per day
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.b2_cloud-breakout-after-a-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
