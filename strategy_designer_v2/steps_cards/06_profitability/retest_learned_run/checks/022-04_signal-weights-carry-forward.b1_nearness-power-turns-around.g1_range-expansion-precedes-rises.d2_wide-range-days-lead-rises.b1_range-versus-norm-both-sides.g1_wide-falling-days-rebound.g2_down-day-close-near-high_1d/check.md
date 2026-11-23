---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4422 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.112 | above 0 | no |
| Mean daily return, on days in a position | 0.0003274 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2905 | above 0 | yes |
| Calmar | 0.2467 | above 0.75 | no |
| Trades per day | 0.4684 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.263 % |
| Yearly return | +8.0 % (over 7.94 years) |
| Days in a position | 89 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
