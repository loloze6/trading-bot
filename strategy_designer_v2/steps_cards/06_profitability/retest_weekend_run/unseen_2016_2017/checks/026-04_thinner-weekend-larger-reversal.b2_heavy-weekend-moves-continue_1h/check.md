---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.709 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.525 | above 0 | no |
| Mean daily return, on days in a position | 0.003319 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.342 | above 0 | yes |
| Calmar | 3.116 | above 0.75 | yes |
| Trades per day | 0.05778 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.608 % |
| Yearly return | +21.1 % (over 1.99 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_2016_2017/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
