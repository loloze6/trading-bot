---
backtest: 044-02_agitated-down-day-range-rebound_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.205 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2011 | above 0 | yes |
| Mean daily return, on days in a position | 0.001661 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.894 | above 0 | yes |
| Calmar | 0.9215 | above 0.75 | yes |
| Trades per day | 0.181 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.929 % |
| Yearly return | +21.9 % (over 5.96 years) |
| Days in a position | 35 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_coins/backtests/044-02_agitated-down-day-range-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
