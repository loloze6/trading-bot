---
backtest: 050-01_falling-calm-scaled-week-fall-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3082 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2614 | above 0 | no |
| Mean daily return, on days in a position | 0.0006301 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.05757 | above 0 | yes |
| Calmar | 0.1713 | above 0.75 | no |
| Trades per day | 0.08099 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.832 % |
| Yearly return | +3.7 % (over 7.94 years) |
| Days in a position | 21 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night7_panic_run/backtests/050-01_falling-calm-scaled-week-fall-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
