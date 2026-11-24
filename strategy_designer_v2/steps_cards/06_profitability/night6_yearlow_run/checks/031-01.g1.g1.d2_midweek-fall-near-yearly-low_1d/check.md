---
backtest: 031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8367 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2671 | above 0 | yes |
| Mean daily return, on days in a position | 0.001167 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6332 | above 0 | yes |
| Calmar | 0.4164 | above 0.75 | no |
| Trades per day | 0.09649 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.520 % |
| Yearly return | +8.1 % (over 7.94 years) |
| Days in a position | 20 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
