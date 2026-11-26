---
backtest: 061-01.g1.d1.g1_day-move-follow-through-both-sides_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1513 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4028 | above 0 | no |
| Mean daily return, on days in a position | 0.0001474 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.02078 | above 0 | yes |
| Calmar | -0.01382 | above 0.75 | no |
| Trades per day | 0.4171 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.859 % |
| Yearly return | -0.9 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.g1_day-move-follow-through-both-sides_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
