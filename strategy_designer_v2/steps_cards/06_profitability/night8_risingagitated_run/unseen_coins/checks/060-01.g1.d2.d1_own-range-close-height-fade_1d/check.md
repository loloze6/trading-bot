---
backtest: 060-01.g1.d2.d1_own-range-close-height-fade_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.06777 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.936 | above 0 | no |
| Mean daily return, on days in a position | 0.0003969 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.2205 | above 0 | no |
| Calmar | 0.008906 | above 0.75 | no |
| Trades per day | 0.02046 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.450 % |
| Yearly return | +0.2 % (over 5.96 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_coins/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
