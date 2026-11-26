---
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.696 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.69 | above 0 | no |
| Mean daily return, on days in a position | -0.00132 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.9075 | above 0 | no |
| Calmar | -0.519 | above 0.75 | no |
| Trades per day | 0.09518 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 3.624 % |
| Yearly return | -51.8 % (over 6.95 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/retest_settlement_run/unseen_coins/backtests/017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
