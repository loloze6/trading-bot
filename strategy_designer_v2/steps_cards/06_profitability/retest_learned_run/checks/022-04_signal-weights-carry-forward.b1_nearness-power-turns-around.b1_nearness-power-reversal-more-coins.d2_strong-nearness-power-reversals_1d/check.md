---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4328 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.09972 | above 0 | no |
| Mean daily return, on days in a position | 0.000374 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.2808 | above 0 | yes |
| Calmar | 0.1874 | above 0.75 | no |
| Trades per day | 0.1863 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.460 % |
| Yearly return | +8.4 % (over 7.94 years) |
| Days in a position | 88 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
