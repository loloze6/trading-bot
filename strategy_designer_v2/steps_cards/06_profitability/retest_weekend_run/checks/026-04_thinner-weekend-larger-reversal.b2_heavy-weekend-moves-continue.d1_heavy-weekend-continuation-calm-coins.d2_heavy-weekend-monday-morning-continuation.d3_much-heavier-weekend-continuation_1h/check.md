---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.447 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1068 | above 0 | no |
| Mean daily return, on days in a position | 0.0004736 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.274 | above 0 | yes |
| Calmar | 0.3621 | above 0.75 | no |
| Trades per day | 0.03749 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.283 % |
| Yearly return | +2.3 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
