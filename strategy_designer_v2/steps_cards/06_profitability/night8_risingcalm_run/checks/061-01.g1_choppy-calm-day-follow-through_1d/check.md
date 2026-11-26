---
backtest: 061-01.g1_choppy-calm-day-follow-through_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1259 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6955 | above 0 | no |
| Mean daily return, on days in a position | -0.0001852 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.268 | above 0 | no |
| Calmar | -0.08523 | above 0.75 | no |
| Trades per day | 0.09748 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.684 % |
| Yearly return | -2.5 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1_choppy-calm-day-follow-through_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
