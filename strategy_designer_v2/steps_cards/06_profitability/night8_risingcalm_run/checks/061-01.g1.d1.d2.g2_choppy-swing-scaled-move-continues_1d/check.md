---
backtest: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2403 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3139 | above 0 | no |
| Mean daily return, on days in a position | 0.0003478 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.06906 | above 0 | yes |
| Calmar | 0.09224 | above 0.75 | no |
| Trades per day | 0.152 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.982 % |
| Yearly return | +2.8 % (over 7.94 years) |
| Days in a position | 35 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
