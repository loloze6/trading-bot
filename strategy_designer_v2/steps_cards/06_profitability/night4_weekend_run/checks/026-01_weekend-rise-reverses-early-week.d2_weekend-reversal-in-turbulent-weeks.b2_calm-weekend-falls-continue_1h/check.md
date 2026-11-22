---
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.008519 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5452 | above 0 | no |
| Mean daily return | 1.723e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2751 | above 0 | no |
| Calmar | -0.0165 | above 0.75 | no |
| Trades per day | 0.04862 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
