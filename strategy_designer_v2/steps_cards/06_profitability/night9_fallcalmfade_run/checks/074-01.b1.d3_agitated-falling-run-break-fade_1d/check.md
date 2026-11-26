---
backtest: 074-01.b1.d3_agitated-falling-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8155 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2458 | above 0 | yes |
| Mean daily return, on days in a position | 0.002861 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6296 | above 0 | yes |
| Calmar | 0.6136 | above 0.75 | no |
| Trades per day | 0.01911 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.257 % |
| Yearly return | +4.0 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d3_agitated-falling-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
