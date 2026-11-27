---
backtest: 074-01.b1.g1_convex-deep-run-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.1 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5463 | above 0 | yes |
| Mean daily return, on days in a position | 0.003197 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9028 | above 0 | yes |
| Calmar | 1.271 | above 0.75 | yes |
| Trades per day | 0.03407 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.383 % |
| Yearly return | +8.1 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.g1_convex-deep-run-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
