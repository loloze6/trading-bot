---
backtest: 062-01_rising-volume-shrink-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5635 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.009339 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008802 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2074 | above 0 | yes |
| Calmar | 0.1679 | above 0.75 | no |
| Trades per day | 0.05507 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.575 % |
| Yearly return | +5.8 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/062-01_rising-volume-shrink-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
