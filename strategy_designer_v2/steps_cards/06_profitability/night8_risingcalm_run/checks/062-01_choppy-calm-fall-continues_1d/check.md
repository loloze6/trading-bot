---
backtest: 062-01_choppy-calm-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0376 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.532 | above 0 | no |
| Mean daily return, on days in a position | 7.431e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1707 | above 0 | no |
| Calmar | -0.007324 | above 0.75 | no |
| Trades per day | 0.06293 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.581 % |
| Yearly return | -0.2 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/062-01_choppy-calm-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
