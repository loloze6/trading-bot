---
backtest: 031-04.g2_sharp-daily-fall-reverses_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6484 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.09428 | above 0 | yes |
| Mean daily return, on days in a position | 0.0007005 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5023 | above 0 | yes |
| Calmar | 0.5025 | above 0.75 | no |
| Trades per day | 0.3942 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.460 % |
| Yearly return | +15.2 % (over 7.94 years) |
| Days in a position | 71 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-04.g2_sharp-daily-fall-reverses_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
