---
backtest: 074-01.b1.d2_run-break-fade-steep-slide_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8831 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.329 | above 0 | yes |
| Mean daily return, on days in a position | 0.001997 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.657 | above 0 | yes |
| Calmar | 0.7686 | above 0.75 | yes |
| Trades per day | 0.04508 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.394 % |
| Yearly return | +6.6 % (over 7.94 years) |
| Days in a position | 9 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d2_run-break-fade-steep-slide_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
