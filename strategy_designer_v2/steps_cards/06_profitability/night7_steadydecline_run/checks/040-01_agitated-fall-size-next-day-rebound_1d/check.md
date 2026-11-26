---
backtest: 040-01_agitated-fall-size-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8926 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.323 | above 0 | yes |
| Mean daily return, on days in a position | 0.001291 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7892 | above 0 | yes |
| Calmar | 0.7469 | above 0.75 | no |
| Trades per day | 0.1787 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.942 % |
| Yearly return | +15.5 % (over 7.94 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/040-01_agitated-fall-size-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
