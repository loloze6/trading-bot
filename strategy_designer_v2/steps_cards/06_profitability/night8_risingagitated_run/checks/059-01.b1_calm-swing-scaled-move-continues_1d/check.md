---
backtest: 059-01.b1_calm-swing-scaled-move-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5538 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.01577 | above 0 | no |
| Mean daily return, on days in a position | 0.000723 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4381 | above 0 | yes |
| Calmar | 0.2727 | above 0.75 | no |
| Trades per day | 0.2528 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.427 % |
| Yearly return | +12.1 % (over 7.94 years) |
| Days in a position | 57 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/059-01.b1_calm-swing-scaled-move-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
