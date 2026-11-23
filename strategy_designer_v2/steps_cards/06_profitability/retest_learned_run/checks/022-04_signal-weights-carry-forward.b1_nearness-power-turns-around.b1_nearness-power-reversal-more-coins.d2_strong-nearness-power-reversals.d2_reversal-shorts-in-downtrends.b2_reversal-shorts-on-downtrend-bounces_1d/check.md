---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1189 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3969 | above 0 | no |
| Mean daily return, on days in a position | 0.0001561 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.01646 | above 0 | yes |
| Calmar | 0.02661 | above 0.75 | no |
| Trades per day | 0.03154 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.479 % |
| Yearly return | +0.7 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
