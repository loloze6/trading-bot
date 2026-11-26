---
backtest: 058-03.e2_choppy-market-distance-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1673 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3869 | above 0 | no |
| Mean daily return, on days in a position | 0.000243 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.005198 | above 0 | no |
| Calmar | 0.02334 | above 0.75 | no |
| Trades per day | 0.1029 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.194 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-03.e2_choppy-market-distance-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
