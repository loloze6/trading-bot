---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.402 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3496 | above 0 | no |
| Mean daily return, on days in a position | 0.004581 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 3.021 | above 0 | yes |
| Calmar | 9.235 | above 0.75 | yes |
| Trades per day | 0.3618 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.163 % |
| Yearly return | +274.3 % (over 1.99 years) |
| Days in a position | 84 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/retest_learned_run/unseen_2016_2017/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
