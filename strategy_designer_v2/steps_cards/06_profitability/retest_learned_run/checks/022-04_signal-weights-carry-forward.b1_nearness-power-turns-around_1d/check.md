---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7674 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1786 | above 0 | yes |
| Mean daily return, on days in a position | 0.000587 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6345 | above 0 | yes |
| Calmar | 0.3779 | above 0.75 | no |
| Trades per day | 0.2198 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.356 % |
| Yearly return | +18.0 % (over 7.94 years) |
| Days in a position | 93 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
