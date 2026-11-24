---
backtest: 031-01.b2_wide-doji-continues-strong-run_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8284 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2742 | above 0 | yes |
| Mean daily return, on days in a position | 0.001948 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7187 | above 0 | yes |
| Calmar | 0.6173 | above 0.75 | no |
| Trades per day | 0.007247 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.206 % |
| Yearly return | +3.2 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-01.b2_wide-doji-continues-strong-run_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
