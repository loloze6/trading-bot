---
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1h bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4167 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.41 | above 0 | no |
| Mean daily return, on days in a position | -0.0003716 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6312 | above 0 | no |
| Calmar | -0.2105 | above 0.75 | no |
| Trades per day | 1.61 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.687 % |
| Yearly return | -17.0 % (over 6.95 years) |
| Days in a position | 99 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_coins/backtests/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
