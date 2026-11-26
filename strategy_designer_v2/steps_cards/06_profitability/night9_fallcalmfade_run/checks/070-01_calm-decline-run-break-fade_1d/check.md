---
backtest: 070-01_calm-decline-run-break-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3011 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2685 | above 0 | no |
| Mean daily return, on days in a position | 0.0003975 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.03172 | above 0 | no |
| Calmar | 0.1844 | above 0.75 | no |
| Trades per day | 0.04871 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.249 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01_calm-decline-run-break-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
