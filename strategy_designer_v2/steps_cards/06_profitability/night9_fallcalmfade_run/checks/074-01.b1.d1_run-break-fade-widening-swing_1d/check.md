---
backtest: 074-01.b1.d1_run-break-fade-widening-swing_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6714 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1173 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009267 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3639 | above 0 | yes |
| Calmar | 0.4829 | above 0.75 | no |
| Trades per day | 0.09387 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.500 % |
| Yearly return | +6.1 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d1_run-break-fade-widening-swing_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
