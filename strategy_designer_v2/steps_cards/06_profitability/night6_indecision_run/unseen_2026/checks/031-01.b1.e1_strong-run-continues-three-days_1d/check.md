---
backtest: 031-01.b1.e1_strong-run-continues-three-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5505 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4524 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006783 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -1.186 | above 0 | no |
| Calmar | 0.6022 | above 0.75 | no |
| Trades per day | 0.298 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.507 % |
| Yearly return | +12.6 % (over 0.87 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2026/backtests/031-01.b1.e1_strong-run-continues-three-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
