---
backtest: 072-03.b1_choppy-deep-bounce-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4243 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9784 | above 0 | no |
| Mean daily return, on days in a position | -0.00383 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4521 | above 0 | no |
| Calmar | -0.3432 | above 0.75 | no |
| Trades per day | 0.05341 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 6.652 % |
| Yearly return | -100.0 % (over 7.94 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03.b1_choppy-deep-bounce-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
