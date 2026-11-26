---
backtest: 061-01.g1.d1.d2_calm-big-rise-near-highs_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.167 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.4026 | above 0 | no |
| Mean daily return, on days in a position | 0.0002991 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.008838 | above 0 | yes |
| Calmar | 0.03854 | above 0.75 | no |
| Trades per day | 0.06269 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.696 % |
| Yearly return | +1.3 % (over 7.94 years) |
| Days in a position | 20 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2_calm-big-rise-near-highs_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
