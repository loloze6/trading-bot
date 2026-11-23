---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9143 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3985 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009035 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7689 | above 0 | yes |
| Calmar | 0.6182 | above 0.75 | no |
| Trades per day | 0.1065 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.216 % |
| Yearly return | +20.4 % (over 7.94 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
