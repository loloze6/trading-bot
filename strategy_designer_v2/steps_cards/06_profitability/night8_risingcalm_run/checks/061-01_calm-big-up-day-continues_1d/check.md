---
backtest: 061-01_calm-big-up-day-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5484 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02116 | above 0 | no |
| Mean daily return, on days in a position | 0.0007047 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4619 | above 0 | yes |
| Calmar | 0.3379 | above 0.75 | no |
| Trades per day | 0.2401 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.420 % |
| Yearly return | +11.9 % (over 7.94 years) |
| Days in a position | 58 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01_calm-big-up-day-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
