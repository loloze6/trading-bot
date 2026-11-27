---
backtest: 074-01.b1.g1_convex-deep-run-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.05296 | above 0 | yes |
| Sharpe minus holding's Sharpe | -3.698 | above 0 | no |
| Mean daily return, on days in a position | 0.0001675 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5136 | above 0 | no |
| Calmar | 0.04401 | above 0.75 | no |
| Trades per day | 0.01026 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.124 % |
| Yearly return | +0.1 % (over 1.99 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.g1_convex-deep-run-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
