---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5705 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01638 | above 0 | yes |
| Mean daily return, on days in a position | 0.0001453 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4647 | above 0 | yes |
| Calmar | 0.3382 | above 0.75 | no |
| Trades per day | 0.256 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.398 % |
| Yearly return | +4.1 % (over 7.94 years) |
| Days in a position | 82 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
