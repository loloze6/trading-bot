---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.118 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.052 | above 0 | yes |
| Mean daily return, on days in a position | 0.001282 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.05723 | above 0 | no |
| Calmar | 1.591 | above 0.75 | yes |
| Trades per day | 0.2871 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.505 % |
| Yearly return | +32.5 % (over 0.87 years) |
| Days in a position | 69 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/retest_learned_run/unseen_2026/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
