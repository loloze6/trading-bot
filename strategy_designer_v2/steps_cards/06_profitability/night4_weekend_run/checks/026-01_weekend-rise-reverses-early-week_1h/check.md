---
backtest: 026-01_weekend-rise-reverses-early-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6755 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.229 | above 0 | no |
| Mean daily return | -0.0002337 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.8042 | above 0 | no |
| Calmar | -0.1461 | above 0.75 | no |
| Trades per day | 0.1203 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
