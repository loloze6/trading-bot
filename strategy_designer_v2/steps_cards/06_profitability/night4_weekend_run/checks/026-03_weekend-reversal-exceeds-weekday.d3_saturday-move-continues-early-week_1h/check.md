---
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.078 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5246 | above 0 | yes |
| Mean daily return | 0.0004223 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.9561 | above 0 | yes |
| Calmar | 0.6124 | above 0.75 | no |
| Trades per day | 0.1965 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
