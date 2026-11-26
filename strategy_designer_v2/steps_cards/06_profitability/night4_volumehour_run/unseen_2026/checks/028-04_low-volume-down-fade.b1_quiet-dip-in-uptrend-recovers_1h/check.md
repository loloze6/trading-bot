---
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2405 | above 0 | no |
| Sharpe minus holding's Sharpe | 0.3814 | above 0 | yes |
| Mean daily return, on days in a position | -0.0003817 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7177 | above 0 | no |
| Calmar | -0.5329 | above 0.75 | no |
| Trades per day | 1.104 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.341 % |
| Yearly return | -9.0 % (over 0.87 years) |
| Days in a position | 44 % of the coins' days |

- Decided by: failed: Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_volumehour_run/unseen_2026/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
