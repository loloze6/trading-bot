---
backtest: 064-01.g1_calm-decline-up-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5294 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.099 | above 0 | no |
| Mean daily return, on days in a position | -0.0009505 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6619 | above 0 | no |
| Calmar | -0.142 | above 0.75 | no |
| Trades per day | 0.07848 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.598 % |
| Yearly return | -6.5 % (over 7.94 years) |
| Days in a position | 17 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01.g1_calm-decline-up-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
