---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.082 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5281 | above 0 | yes |
| Mean daily return, on days in a position | 0.002387 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9636 | above 0 | yes |
| Calmar | 0.9857 | above 0.75 | yes |
| Trades per day | 0.02887 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.370 % |
| Yearly return | +7.7 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
