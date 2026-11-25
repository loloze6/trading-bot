---
backtest: 039-01_agitated-swing-fall-low-close-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8745 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3049 | above 0 | yes |
| Mean daily return, on days in a position | 0.001481 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7625 | above 0 | yes |
| Calmar | 0.6849 | above 0.75 | no |
| Trades per day | 0.1769 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.106 % |
| Yearly return | +17.6 % (over 7.94 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/039-01_agitated-swing-fall-low-close-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
