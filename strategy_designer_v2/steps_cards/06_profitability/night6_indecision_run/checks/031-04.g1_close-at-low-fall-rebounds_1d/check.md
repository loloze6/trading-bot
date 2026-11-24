---
backtest: 031-04.g1_close-at-low-fall-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5476 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.006615 | above 0 | no |
| Mean daily return, on days in a position | 0.002208 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.471 | above 0 | yes |
| Calmar | 0.5696 | above 0.75 | no |
| Trades per day | 0.02665 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.422 % |
| Yearly return | +4.2 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-04.g1_close-at-low-fall-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
