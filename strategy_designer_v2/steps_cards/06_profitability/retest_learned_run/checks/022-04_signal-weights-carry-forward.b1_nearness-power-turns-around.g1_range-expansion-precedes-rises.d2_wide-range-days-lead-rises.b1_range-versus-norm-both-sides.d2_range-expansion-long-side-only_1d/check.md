---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8528 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2986 | above 0 | yes |
| Mean daily return, on days in a position | 0.001093 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6818 | above 0 | yes |
| Calmar | 0.6414 | above 0.75 | no |
| Trades per day | 0.3403 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.792 % |
| Yearly return | +26.3 % (over 7.94 years) |
| Days in a position | 73 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
