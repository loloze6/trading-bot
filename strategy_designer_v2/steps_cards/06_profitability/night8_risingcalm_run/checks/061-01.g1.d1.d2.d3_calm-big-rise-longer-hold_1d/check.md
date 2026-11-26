---
backtest: 061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3474 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2222 | above 0 | no |
| Mean daily return, on days in a position | 0.0007469 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1358 | above 0 | yes |
| Calmar | 0.1243 | above 0.75 | no |
| Trades per day | 0.04352 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.166 % |
| Yearly return | +5.4 % (over 7.94 years) |
| Days in a position | 28 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
