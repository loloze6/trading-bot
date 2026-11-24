---
backtest: 031-01.g1.g2_monthly-trend-carries-into-saturday_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5704 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01628 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008005 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4057 | above 0 | yes |
| Calmar | 0.4434 | above 0.75 | no |
| Trades per day | 0.1211 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.656 % |
| Yearly return | +6.6 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g2_monthly-trend-carries-into-saturday_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
