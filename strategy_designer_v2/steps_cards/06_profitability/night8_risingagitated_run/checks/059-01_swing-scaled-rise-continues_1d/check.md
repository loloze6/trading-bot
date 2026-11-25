---
backtest: 059-01_swing-scaled-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5322 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.02199 | above 0 | no |
| Mean daily return, on days in a position | 0.0005342 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.437 | above 0 | yes |
| Calmar | 0.2805 | above 0.75 | no |
| Trades per day | 0.443 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.915 % |
| Yearly return | +13.7 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/059-01_swing-scaled-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
