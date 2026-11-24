---
backtest: 031-01.g1.g1.g1.g2_thursday-run-carries-two-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6964 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1422 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008354 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.541 | above 0 | yes |
| Calmar | 0.4554 | above 0.75 | no |
| Trades per day | 0.1845 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.981 % |
| Yearly return | +12.0 % (over 7.94 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.g2_thursday-run-carries-two-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
