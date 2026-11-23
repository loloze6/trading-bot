---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d3_wide-uptrend-days-held-longer_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.015 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4612 | above 0 | yes |
| Mean daily return, on days in a position | 0.0003984 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.8195 | above 0 | yes |
| Calmar | 0.9837 | above 0.75 | yes |
| Trades per day | 0.07978 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.425 % |
| Yearly return | +8.2 % (over 7.94 years) |
| Days in a position | 57 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d3_wide-uptrend-days-held-longer_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
