---
backtest: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.147 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5929 | above 0 | yes |
| Mean daily return, on days in a position | 0.001568 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.006 | above 0 | yes |
| Calmar | 1.898 | above 0.75 | yes |
| Trades per day | 0.09205 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.686 % |
| Yearly return | +15.3 % (over 7.94 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
