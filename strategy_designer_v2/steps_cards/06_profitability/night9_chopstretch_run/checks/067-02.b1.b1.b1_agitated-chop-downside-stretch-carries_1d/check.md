---
backtest: 067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2745 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8441 | above 0 | no |
| Mean daily return, on days in a position | -0.0008207 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.7098 | above 0 | no |
| Calmar | -0.1154 | above 0.75 | no |
| Trades per day | 0.02925 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.432 % |
| Yearly return | -2.6 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
