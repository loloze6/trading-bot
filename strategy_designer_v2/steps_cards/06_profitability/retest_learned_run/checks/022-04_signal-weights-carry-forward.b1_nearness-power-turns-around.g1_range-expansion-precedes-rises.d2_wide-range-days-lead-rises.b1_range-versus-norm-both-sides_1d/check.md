---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7055 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1513 | above 0 | yes |
| Mean daily return, on days in a position | 0.0001554 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.5909 | above 0 | yes |
| Calmar | 0.4201 | above 0.75 | no |
| Trades per day | 0.343 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.416 % |
| Yearly return | +5.4 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
