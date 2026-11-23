---
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7464 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6484 | above 0 | yes |
| Mean daily return, on days in a position | 0.0004216 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1437 | above 0 | no |
| Calmar | 1.225 | above 0.75 | yes |
| Trades per day | 0.1833 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.031 % |
| Yearly return | +13.6 % (over 0.87 years) |
| Days in a position | 96 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
