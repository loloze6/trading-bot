---
backtest: 074-01.b1_falling-deep-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7136 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1594 | above 0 | yes |
| Mean daily return, on days in a position | 0.001139 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4498 | above 0 | yes |
| Calmar | 0.459 | above 0.75 | no |
| Trades per day | 0.07989 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.493 % |
| Yearly return | +6.5 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1_falling-deep-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
