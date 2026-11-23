---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1188 | above 0 | no |
| Sharpe minus holding's Sharpe | -3.353 | above 0 | no |
| Mean daily return, on days in a position | -0.0001734 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5692 | above 0 | no |
| Calmar | -0.127 | above 0.75 | no |
| Trades per day | 0.02027 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.190 % |
| Yearly return | -0.5 % (over 1.99 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_2016_2017/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
