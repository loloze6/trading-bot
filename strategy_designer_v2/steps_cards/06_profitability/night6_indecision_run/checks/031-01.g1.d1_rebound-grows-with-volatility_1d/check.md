---
backtest: 031-01.g1.d1_rebound-grows-with-volatility_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.059 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5052 | above 0 | yes |
| Mean daily return, on days in a position | 0.00398 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9454 | above 0 | yes |
| Calmar | 0.9559 | above 0.75 | yes |
| Trades per day | 0.03401 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.488 % |
| Yearly return | +9.9 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.g1.d1_rebound-grows-with-volatility_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
