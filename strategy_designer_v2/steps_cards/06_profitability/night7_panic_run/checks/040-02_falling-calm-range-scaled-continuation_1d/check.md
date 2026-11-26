---
backtest: 040-02_falling-calm-range-scaled-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2202 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3494 | above 0 | no |
| Mean daily return, on days in a position | 0.000419 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.1002 | above 0 | yes |
| Calmar | 0.08694 | above 0.75 | no |
| Trades per day | 0.09037 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.793 % |
| Yearly return | +2.2 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/040-02_falling-calm-range-scaled-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
