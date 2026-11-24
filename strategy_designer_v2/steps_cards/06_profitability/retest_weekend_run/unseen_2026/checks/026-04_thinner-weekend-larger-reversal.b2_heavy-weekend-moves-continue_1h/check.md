---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8539 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.7559 | above 0 | yes |
| Mean daily return, on days in a position | 0.002408 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1281 | above 0 | no |
| Calmar | 1.985 | above 0.75 | yes |
| Trades per day | 0.03063 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.336 % |
| Yearly return | +5.4 % (over 0.87 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_2026/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
