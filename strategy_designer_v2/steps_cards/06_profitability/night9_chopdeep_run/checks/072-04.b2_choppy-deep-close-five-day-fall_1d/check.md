---
backtest: 072-04.b2_choppy-deep-close-five-day-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.08937 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6435 | above 0 | no |
| Mean daily return, on days in a position | -0.0001396 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3038 | above 0 | no |
| Calmar | -0.07558 | above 0.75 | no |
| Trades per day | 0.1273 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.977 % |
| Yearly return | -3.3 % (over 7.94 years) |
| Days in a position | 33 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-04.b2_choppy-deep-close-five-day-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
