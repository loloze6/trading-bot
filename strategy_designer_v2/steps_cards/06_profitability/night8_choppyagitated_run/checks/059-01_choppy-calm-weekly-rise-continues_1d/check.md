---
backtest: 059-01_choppy-calm-weekly-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4123 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1573 | above 0 | no |
| Mean daily return, on days in a position | 0.0008687 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.252 | above 0 | yes |
| Calmar | 0.1792 | above 0.75 | no |
| Trades per day | 0.05279 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.760 % |
| Yearly return | +5.1 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01_choppy-calm-weekly-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
