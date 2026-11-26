---
backtest: 074-01.g1.d1_wide-close-high-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8154 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2458 | above 0 | yes |
| Mean daily return, on days in a position | 0.003285 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6427 | above 0 | yes |
| Calmar | 0.7675 | above 0.75 | yes |
| Trades per day | 0.01427 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.217 % |
| Yearly return | +3.3 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.g1.d1_wide-close-high-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
