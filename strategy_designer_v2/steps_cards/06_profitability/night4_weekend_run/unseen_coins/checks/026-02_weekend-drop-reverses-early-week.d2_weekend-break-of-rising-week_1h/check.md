---
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.06283 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.057 | above 0 | no |
| Mean daily return, on days in a position | -0.0002118 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5412 | above 0 | no |
| Calmar | -0.04441 | above 0.75 | no |
| Trades per day | 0.05251 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.533 % |
| Yearly return | -1.1 % (over 6.95 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_coins/backtests/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
