---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8861 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3324 | above 0 | yes |
| Mean daily return | 0.0002411 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.7518 | above 0 | yes |
| Calmar | 0.61 | above 0.75 | no |
| Trades per day | 0.04342 | at least 0.01 | yes |

- Decided by: failed: Mean daily return; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
