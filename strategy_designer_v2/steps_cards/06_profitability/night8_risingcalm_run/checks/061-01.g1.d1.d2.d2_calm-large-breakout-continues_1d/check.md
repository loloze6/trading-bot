---
backtest: 061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1634 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4062 | above 0 | no |
| Mean daily return, on days in a position | 0.0006711 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.02611 | above 0 | no |
| Calmar | 0.04709 | above 0.75 | no |
| Trades per day | 0.0208 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.539 % |
| Yearly return | +1.2 % (over 7.94 years) |
| Days in a position | 7 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
