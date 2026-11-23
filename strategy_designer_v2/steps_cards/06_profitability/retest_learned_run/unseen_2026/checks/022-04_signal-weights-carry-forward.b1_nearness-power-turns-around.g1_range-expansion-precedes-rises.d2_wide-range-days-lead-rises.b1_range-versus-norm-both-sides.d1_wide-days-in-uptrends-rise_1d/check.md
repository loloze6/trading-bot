---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6514 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5533 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009116 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1372 | above 0 | no |
| Calmar | 0.5806 | above 0.75 | no |
| Trades per day | 0.1843 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.281 % |
| Yearly return | +14.0 % (over 0.87 years) |
| Days in a position | 48 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/unseen_2026/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
