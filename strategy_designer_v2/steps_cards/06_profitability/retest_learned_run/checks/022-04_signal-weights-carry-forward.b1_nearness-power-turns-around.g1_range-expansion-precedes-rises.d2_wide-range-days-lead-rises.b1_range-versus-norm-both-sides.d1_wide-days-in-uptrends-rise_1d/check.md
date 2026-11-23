---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.096 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5419 | above 0 | yes |
| Mean daily return, on days in a position | 0.001472 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9127 | above 0 | yes |
| Calmar | 1.302 | above 0.75 | yes |
| Trades per day | 0.2029 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.256 % |
| Yearly return | +26.4 % (over 7.94 years) |
| Days in a position | 49 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
