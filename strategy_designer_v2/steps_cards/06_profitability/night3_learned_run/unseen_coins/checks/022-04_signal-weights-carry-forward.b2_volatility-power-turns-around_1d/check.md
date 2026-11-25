---
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.005303 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9975 | above 0 | no |
| Mean daily return, on days in a position | -3.731e-06 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.1345 | above 0 | no |
| Calmar | -0.05442 | above 0.75 | no |
| Trades per day | 0.1662 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.315 % |
| Yearly return | -3.3 % (over 5.63 years) |
| Days in a position | 98 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night3_learned_run/unseen_coins/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
