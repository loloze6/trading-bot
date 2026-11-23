---
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.05497 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.5823 | above 0 | no |
| Mean daily return, on days in a position | -6.588e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2314 | above 0 | no |
| Calmar | -0.04709 | above 0.75 | no |
| Trades per day | 0.05502 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.725 % |
| Yearly return | -1.7 % (over 7.94 years) |
| Days in a position | 32 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
