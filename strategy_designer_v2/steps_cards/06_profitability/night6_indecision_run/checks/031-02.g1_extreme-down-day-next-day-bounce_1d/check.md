---
backtest: 031-02.g1_extreme-down-day-next-day-bounce_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2566 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2976 | above 0 | no |
| Mean daily return, on days in a position | 0.001618 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1708 | above 0 | yes |
| Calmar | 0.1431 | above 0.75 | no |
| Trades per day | 0.02699 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.665 % |
| Yearly return | +2.5 % (over 7.94 years) |
| Days in a position | 6 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.g1_extreme-down-day-next-day-bounce_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
