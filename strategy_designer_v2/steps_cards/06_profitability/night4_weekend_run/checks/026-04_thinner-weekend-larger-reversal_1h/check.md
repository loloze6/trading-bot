---
backtest: 026-04_thinner-weekend-larger-reversal_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5075 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.061 | above 0 | no |
| Mean daily return | -0.0002737 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.617 | above 0 | no |
| Calmar | -0.1587 | above 0.75 | no |
| Trades per day | 0.2297 | at least 0.01 | yes |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
