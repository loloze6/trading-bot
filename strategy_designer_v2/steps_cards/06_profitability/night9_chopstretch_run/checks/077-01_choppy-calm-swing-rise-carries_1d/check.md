---
backtest: 077-01_choppy-calm-swing-rise-carries_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5164 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.05325 | above 0 | no |
| Mean daily return, on days in a position | 0.002563 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3231 | above 0 | yes |
| Calmar | 0.1875 | above 0.75 | no |
| Trades per day | 0.01602 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.679 % |
| Yearly return | +6.0 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01_choppy-calm-swing-rise-carries_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
