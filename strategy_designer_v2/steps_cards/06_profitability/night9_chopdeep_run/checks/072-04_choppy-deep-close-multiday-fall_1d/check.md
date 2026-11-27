---
backtest: 072-04_choppy-deep-close-multiday-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2224 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7766 | above 0 | no |
| Mean daily return, on days in a position | -0.0003224 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5084 | above 0 | no |
| Calmar | -0.1031 | above 0.75 | no |
| Trades per day | 0.1352 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.870 % |
| Yearly return | -4.9 % (over 7.94 years) |
| Days in a position | 31 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-04_choppy-deep-close-multiday-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
