---
backtest: 064-01_calm-decline-big-rise-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8268 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.396 | above 0 | no |
| Mean daily return, on days in a position | -0.004566 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9854 | above 0 | no |
| Calmar | -0.1304 | above 0.75 | no |
| Trades per day | 0.006118 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.152 % |
| Yearly return | -2.4 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01_calm-decline-big-rise-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
