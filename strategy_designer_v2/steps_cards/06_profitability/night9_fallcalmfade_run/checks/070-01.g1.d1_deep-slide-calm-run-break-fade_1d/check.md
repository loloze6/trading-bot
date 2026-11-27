---
backtest: 070-01.g1.d1_deep-slide-calm-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5172 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05236 | above 0 | no |
| Mean daily return, on days in a position | 0.004452 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2843 | above 0 | yes |
| Calmar | 0.3849 | above 0.75 | no |
| Trades per day | 0.006584 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.220 % |
| Yearly return | +2.1 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d1_deep-slide-calm-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
