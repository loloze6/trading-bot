---
backtest: 031-01_near-yearly-low-keeps-falling_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2983 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8799 | above 0 | no |
| Mean daily return, on days in a position | -0.0003516 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5044 | above 0 | no |
| Calmar | -0.1855 | above 0.75 | no |
| Trades per day | 0.07123 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.946 % |
| Yearly return | -16.4 % (over 7.94 years) |
| Days in a position | 86 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01_near-yearly-low-keeps-falling_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
