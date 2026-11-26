---
backtest: 058-01_agitated-decline-rally-giveback_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2963 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8659 | above 0 | no |
| Mean daily return, on days in a position | -0.0005423 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3842 | above 0 | no |
| Calmar | -0.08674 | above 0.75 | no |
| Trades per day | 0.04795 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.473 % |
| Yearly return | -3.0 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01_agitated-decline-rally-giveback_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
