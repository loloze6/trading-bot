---
backtest: 061-01.g1.g3_calm-big-fall-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5195 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05007 | above 0 | no |
| Mean daily return, on days in a position | 0.001058 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3637 | above 0 | yes |
| Calmar | 0.2345 | above 0.75 | no |
| Trades per day | 0.06765 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.322 % |
| Yearly return | +14.1 % (over 7.94 years) |
| Days in a position | 60 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.g3_calm-big-fall-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
