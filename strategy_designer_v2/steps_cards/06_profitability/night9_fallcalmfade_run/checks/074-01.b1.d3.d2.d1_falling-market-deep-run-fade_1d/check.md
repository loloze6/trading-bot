---
backtest: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9797 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4255 | above 0 | yes |
| Mean daily return, on days in a position | 0.002159 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.752 | above 0 | yes |
| Calmar | 0.9184 | above 0.75 | yes |
| Trades per day | 0.04885 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.415 % |
| Yearly return | +7.7 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
