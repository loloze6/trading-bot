---
backtest: 033-03.b2_rising-market-range-top-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.734 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.636 | above 0 | yes |
| Mean daily return, on days in a position | 0.002183 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7448 | above 0 | yes |
| Calmar | 5.769 | above 0.75 | yes |
| Trades per day | 0.1854 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.095 % |
| Yearly return | +40.7 % (over 0.87 years) |
| Days in a position | 46 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/033-03.b2_rising-market-range-top-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
