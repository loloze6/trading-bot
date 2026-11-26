---
backtest: 039-02.d1_wide-range-low-close-next-day-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.209 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2047 | above 0 | yes |
| Mean daily return, on days in a position | 0.001885 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.918 | above 0 | yes |
| Calmar | 1.22 | above 0.75 | yes |
| Trades per day | 0.3048 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.376 % |
| Yearly return | +32.8 % (over 5.96 years) |
| Days in a position | 46 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_coins/backtests/039-02.d1_wide-range-low-close-next-day-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
