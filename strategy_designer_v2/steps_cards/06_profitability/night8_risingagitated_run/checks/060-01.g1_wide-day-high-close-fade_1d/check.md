---
backtest: 060-01.g1_wide-day-high-close-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6097 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.04007 | above 0 | yes |
| Mean daily return, on days in a position | 0.005535 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4371 | above 0 | yes |
| Calmar | 0.3798 | above 0.75 | no |
| Trades per day | 0.005127 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.179 % |
| Yearly return | +2.0 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1_wide-day-high-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
