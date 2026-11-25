---
backtest: 036-02_range-scaled-rally-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7403 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1862 | above 0 | yes |
| Mean daily return, on days in a position | 0.001018 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5632 | above 0 | yes |
| Calmar | 0.4051 | above 0.75 | no |
| Trades per day | 0.2223 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.265 % |
| Yearly return | +25.4 % (over 7.94 years) |
| Days in a position | 86 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/036-02_range-scaled-rally-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
