---
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5335 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02019 | above 0 | no |
| Mean daily return, on days in a position | 0.0006145 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3134 | above 0 | yes |
| Calmar | 0.5017 | above 0.75 | no |
| Trades per day | 0.02739 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.214 % |
| Yearly return | +2.1 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
