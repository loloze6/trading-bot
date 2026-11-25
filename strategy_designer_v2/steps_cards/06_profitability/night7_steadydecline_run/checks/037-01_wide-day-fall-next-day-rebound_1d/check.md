---
backtest: 037-01_wide-day-fall-next-day-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7794 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2252 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009901 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6226 | above 0 | yes |
| Calmar | 0.6876 | above 0.75 | no |
| Trades per day | 0.3721 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.676 % |
| Yearly return | +21.8 % (over 7.94 years) |
| Days in a position | 69 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/037-01_wide-day-fall-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
