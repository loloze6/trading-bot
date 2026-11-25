---
backtest: 051-01_falling-agitated-scaled-fall-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.049 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4795 | above 0 | yes |
| Mean daily return, on days in a position | 0.002042 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9013 | above 0 | yes |
| Calmar | 0.7684 | above 0.75 | yes |
| Trades per day | 0.06916 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.528 % |
| Yearly return | +10.6 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_panic_run/backtests/051-01_falling-agitated-scaled-fall-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
