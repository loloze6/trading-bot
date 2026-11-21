---
backtest: 018-06_hourly-plunge-multiday-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6962 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.25 | above 0 | no |
| Mean daily return | -0.001136 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8566 | above 0 | no |
| Calmar | -0.4478 | above 0.75 | no |
| Trades per day | 0.4322 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
