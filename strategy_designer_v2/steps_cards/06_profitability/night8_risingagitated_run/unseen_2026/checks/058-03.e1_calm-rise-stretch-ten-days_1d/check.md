---
backtest: 058-03.e1_calm-rise-stretch-ten-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.563 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.465 | above 0 | yes |
| Mean daily return, on days in a position | 0.002867 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.952 | above 0 | yes |
| Calmar | 3.125 | above 0.75 | yes |
| Trades per day | 0.04777 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.841 % |
| Yearly return | +26.9 % (over 0.87 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2026/backtests/058-03.e1_calm-rise-stretch-ten-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
