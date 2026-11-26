---
backtest: 061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5218 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04779 | above 0 | no |
| Mean daily return, on days in a position | 0.001369 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3618 | above 0 | yes |
| Calmar | 0.2028 | above 0.75 | no |
| Trades per day | 0.08565 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.525 % |
| Yearly return | +11.6 % (over 7.94 years) |
| Days in a position | 30 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
