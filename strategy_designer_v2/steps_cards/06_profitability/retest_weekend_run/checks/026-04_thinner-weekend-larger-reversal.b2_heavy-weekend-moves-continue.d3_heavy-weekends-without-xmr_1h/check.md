---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
data: BTC, ETH, LTC, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9975 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.445 | above 0 | yes |
| Mean daily return, on days in a position | 0.001879 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.88 | above 0 | yes |
| Calmar | 0.796 | above 0.75 | yes |
| Trades per day | 0.0415 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.551 % |
| Yearly return | +10.5 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
