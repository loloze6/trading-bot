---
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.485 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4914 | above 0 | yes |
| Mean daily return, on days in a position | 0.002714 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.234 | above 0 | yes |
| Calmar | 1.895 | above 0.75 | yes |
| Trades per day | 0.2425 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.644 % |
| Yearly return | +52.0 % (over 6.95 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/paying_rerun_run/unseen_coins/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
