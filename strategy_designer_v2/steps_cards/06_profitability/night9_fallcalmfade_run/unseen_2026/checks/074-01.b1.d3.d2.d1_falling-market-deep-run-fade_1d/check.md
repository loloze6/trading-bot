---
backtest: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4026 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3045 | above 0 | yes |
| Mean daily return, on days in a position | 0.0004372 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.09503 | above 0 | no |
| Calmar | 0.6954 | above 0.75 | no |
| Trades per day | 0.05452 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.226 % |
| Yearly return | +1.7 % (over 0.87 years) |
| Days in a position | 11 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2026/backtests/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
