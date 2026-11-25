---
backtest: 054-03.b1_rising-market-reclaimed-low-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1062 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.448 | above 0 | no |
| Mean daily return, on days in a position | 0.0004154 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.03777 | above 0 | no |
| Calmar | 0.03946 | above 0.75 | no |
| Trades per day | 0.005592 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.248 % |
| Yearly return | +0.4 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-03.b1_rising-market-reclaimed-low-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
