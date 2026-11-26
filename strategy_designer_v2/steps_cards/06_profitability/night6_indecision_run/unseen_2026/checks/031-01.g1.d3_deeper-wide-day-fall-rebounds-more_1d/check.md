---
backtest: 031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9944 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8964 | above 0 | yes |
| Mean daily return, on days in a position | 0.005844 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2171 | above 0 | yes |
| Calmar | 2.343 | above 0.75 | yes |
| Trades per day | 0.03946 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.869 % |
| Yearly return | +16.4 % (over 0.87 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
