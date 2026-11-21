---
backtest: 018-05_hourly-plunge-loss-before-close_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -1.214 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.768 | above 0 | no |
| Mean daily return | -0.001183 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.419 | above 0 | no |
| Calmar | -0.3955 | above 0.75 | no |
| Trades per day | 1.38 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
