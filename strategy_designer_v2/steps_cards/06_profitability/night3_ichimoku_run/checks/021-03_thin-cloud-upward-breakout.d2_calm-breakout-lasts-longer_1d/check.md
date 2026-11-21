---
backtest: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9316 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3757 | above 0 | yes |
| Mean daily return | 0.000521 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7426 | above 0 | yes |
| Calmar | 0.6235 | above 0.75 | no |
| Trades per day | 0.01353 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
