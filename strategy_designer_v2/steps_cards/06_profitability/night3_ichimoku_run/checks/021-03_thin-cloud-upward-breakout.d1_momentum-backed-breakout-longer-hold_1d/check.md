---
backtest: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.117 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5512 | above 0 | yes |
| Mean daily return | 0.0003326 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7405 | above 0 | yes |
| Calmar | 0.9451 | above 0.75 | yes |
| Trades per day | 0.006952 | at least 0.01 | no |

- Decided by: failed: Mean daily return; Trades per day
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
