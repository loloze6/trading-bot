---
backtest: 058-03.g1_calm-downtrend-weekly-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5329 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.0367 | above 0 | no |
| Mean daily return, on days in a position | 0.001044 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3491 | above 0 | yes |
| Calmar | 0.3095 | above 0.75 | no |
| Trades per day | 0.1139 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.907 % |
| Yearly return | +8.1 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-03.g1_calm-downtrend-weekly-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
