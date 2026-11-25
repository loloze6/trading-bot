---
backtest: 054-04.b1_reclaimed-low-after-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3818 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1878 | above 0 | no |
| Mean daily return, on days in a position | 0.001152 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1827 | above 0 | yes |
| Calmar | 0.2368 | above 0.75 | no |
| Trades per day | 0.00402 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.141 % |
| Yearly return | +1.0 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-04.b1_reclaimed-low-after-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
