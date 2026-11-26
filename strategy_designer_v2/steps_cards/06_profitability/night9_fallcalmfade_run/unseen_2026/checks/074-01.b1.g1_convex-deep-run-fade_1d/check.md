---
backtest: 074-01.b1.g1_convex-deep-run-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7022 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6042 | above 0 | yes |
| Mean daily return, on days in a position | 0.001127 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3298 | above 0 | yes |
| Calmar | 1.998 | above 0.75 | yes |
| Trades per day | 0.03531 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.217 % |
| Yearly return | +2.9 % (over 0.87 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/074-01.b1.g1_convex-deep-run-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
