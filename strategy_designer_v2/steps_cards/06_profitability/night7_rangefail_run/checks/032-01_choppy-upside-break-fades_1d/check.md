---
backtest: 032-01_choppy-upside-break-fades_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4041 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9582 | above 0 | no |
| Mean daily return, on days in a position | -0.0002818 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5496 | above 0 | no |
| Calmar | -0.08326 | above 0.75 | no |
| Trades per day | 0.007304 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.095 % |
| Yearly return | -0.7 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-01_choppy-upside-break-fades_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
