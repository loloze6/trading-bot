---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.881 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.8701 | above 0 | no |
| Mean daily return, on days in a position | 0.004778 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.466 | above 0 | yes |
| Calmar | 6.627 | above 0.75 | yes |
| Trades per day | 0.2637 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.855 % |
| Yearly return | +160.7 % (over 1.99 years) |
| Days in a position | 59 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/retest_learned_run/unseen_2016_2017/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
