---
backtest: 038-02_calm-scaled-weekly-fall-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.01135 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.581 | above 0 | no |
| Mean daily return, on days in a position | -1.597e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2344 | above 0 | no |
| Calmar | -0.05165 | above 0.75 | no |
| Trades per day | 0.1645 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.144 % |
| Yearly return | -2.6 % (over 7.94 years) |
| Days in a position | 43 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/038-02_calm-scaled-weekly-fall-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
