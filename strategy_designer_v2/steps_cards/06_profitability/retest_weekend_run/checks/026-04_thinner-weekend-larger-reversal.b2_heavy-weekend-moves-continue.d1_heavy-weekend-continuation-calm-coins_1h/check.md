---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8957 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.342 | above 0 | yes |
| Mean daily return, on days in a position | 0.001486 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7643 | above 0 | yes |
| Calmar | 0.6712 | above 0.75 | no |
| Trades per day | 0.04183 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.497 % |
| Yearly return | +8.4 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
