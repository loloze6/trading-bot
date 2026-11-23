---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4315 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1227 | above 0 | no |
| Mean daily return, on days in a position | 0.0001021 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2747 | above 0 | yes |
| Calmar | 0.2214 | above 0.75 | no |
| Trades per day | 0.2652 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.447 % |
| Yearly return | +3.4 % (over 7.94 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
