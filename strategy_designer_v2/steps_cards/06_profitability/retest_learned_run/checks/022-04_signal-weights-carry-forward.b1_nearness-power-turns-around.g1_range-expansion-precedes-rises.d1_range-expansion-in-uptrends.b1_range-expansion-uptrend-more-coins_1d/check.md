---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.064 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4565 | above 0 | yes |
| Mean daily return, on days in a position | 0.001255 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8652 | above 0 | yes |
| Calmar | 0.9389 | above 0.75 | yes |
| Trades per day | 0.2932 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.606 % |
| Yearly return | +32.2 % (over 7.94 years) |
| Days in a position | 71 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
