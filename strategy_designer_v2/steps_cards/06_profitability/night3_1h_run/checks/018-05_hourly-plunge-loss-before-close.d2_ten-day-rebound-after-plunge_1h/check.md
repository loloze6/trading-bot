---
backtest: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.896 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3423 | above 0 | yes |
| Mean daily return | 0.00127 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7306 | above 0 | yes |
| Calmar | 0.6788 | above 0.75 | no |
| Trades per day | 0.06488 | at least 0.01 | yes |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
