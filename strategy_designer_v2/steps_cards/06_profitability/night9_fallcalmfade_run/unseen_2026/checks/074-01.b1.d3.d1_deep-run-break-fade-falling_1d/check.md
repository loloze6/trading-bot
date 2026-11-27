---
backtest: 074-01.b1.d3.d1_deep-run-break-fade-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5788 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4807 | above 0 | yes |
| Mean daily return, on days in a position | 0.001006 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2849 | above 0 | yes |
| Calmar | 1.419 | above 0.75 | yes |
| Trades per day | 0.03323 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.221 % |
| Yearly return | +2.4 % (over 0.87 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/074-01.b1.d3.d1_deep-run-break-fade-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
