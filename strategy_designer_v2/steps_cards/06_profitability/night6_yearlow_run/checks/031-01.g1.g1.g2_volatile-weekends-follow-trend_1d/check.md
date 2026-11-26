---
backtest: 031-01.g1.g1.g2_volatile-weekends-follow-trend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8749 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3207 | above 0 | yes |
| Mean daily return, on days in a position | 0.001361 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7096 | above 0 | yes |
| Calmar | 0.5775 | above 0.75 | no |
| Trades per day | 0.08223 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.650 % |
| Yearly return | +10.6 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2_volatile-weekends-follow-trend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
