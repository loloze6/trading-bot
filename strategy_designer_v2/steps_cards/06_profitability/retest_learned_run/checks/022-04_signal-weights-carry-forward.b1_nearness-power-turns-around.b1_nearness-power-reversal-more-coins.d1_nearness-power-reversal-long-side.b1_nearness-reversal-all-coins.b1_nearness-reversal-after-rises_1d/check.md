---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.033 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5261 | above 0 | yes |
| Mean daily return, on days in a position | 0.001151 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.881 | above 0 | yes |
| Calmar | 0.899 | above 0.75 | yes |
| Trades per day | 0.06536 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.867 % |
| Yearly return | +17.1 % (over 7.94 years) |
| Days in a position | 41 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
