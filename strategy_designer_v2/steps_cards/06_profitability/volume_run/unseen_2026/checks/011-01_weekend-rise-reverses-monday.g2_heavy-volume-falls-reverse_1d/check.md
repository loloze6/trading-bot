---
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.8565 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9545 | above 0 | no |
| Mean daily return, on days in a position | -0.004422 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.123 | above 0 | no |
| Calmar | -0.9418 | above 0.75 | no |
| Trades per day | 0.06386 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.270 % |
| Yearly return | -21.1 % (over 0.87 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/volume_run/unseen_2026/backtests/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
