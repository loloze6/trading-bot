---
backtest: 031-01.g1_wide-day-low-close-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9644 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4102 | above 0 | yes |
| Mean daily return, on days in a position | 0.004609 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8197 | above 0 | yes |
| Calmar | 0.6944 | above 0.75 | no |
| Trades per day | 0.03378 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.624 % |
| Yearly return | +11.4 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.g1_wide-day-low-close-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
