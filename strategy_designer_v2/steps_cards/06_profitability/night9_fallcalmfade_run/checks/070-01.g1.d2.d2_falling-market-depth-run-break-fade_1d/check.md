---
backtest: 070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3713 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1828 | above 0 | no |
| Mean daily return, on days in a position | 0.000228 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.08004 | above 0 | yes |
| Calmar | 0.1807 | above 0.75 | no |
| Trades per day | 0.07909 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.188 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 16 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
