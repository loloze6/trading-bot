---
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4961 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05766 | above 0 | no |
| Mean daily return | 0.0001555 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.3908 | above 0 | yes |
| Calmar | 0.3266 | above 0.75 | no |
| Trades per day | 0.1222 | at least 0.01 | yes |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
