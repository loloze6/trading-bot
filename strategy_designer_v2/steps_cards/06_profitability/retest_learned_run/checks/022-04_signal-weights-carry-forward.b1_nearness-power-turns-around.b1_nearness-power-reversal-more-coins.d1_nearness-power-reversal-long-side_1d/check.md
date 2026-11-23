---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9402 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4077 | above 0 | yes |
| Mean daily return, on days in a position | 0.0009119 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8037 | above 0 | yes |
| Calmar | 0.6152 | above 0.75 | no |
| Trades per day | 0.1045 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.190 % |
| Yearly return | +20.7 % (over 7.94 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
