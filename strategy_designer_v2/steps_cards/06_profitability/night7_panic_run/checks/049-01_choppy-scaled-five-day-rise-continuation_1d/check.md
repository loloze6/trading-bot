---
backtest: 049-01_choppy-scaled-five-day-rise-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4613 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.09291 | above 0 | no |
| Mean daily return, on days in a position | 0.0005821 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3213 | above 0 | yes |
| Calmar | 0.2386 | above 0.75 | no |
| Trades per day | 0.09016 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.623 % |
| Yearly return | +4.9 % (over 7.94 years) |
| Days in a position | 26 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/049-01_choppy-scaled-five-day-rise-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
