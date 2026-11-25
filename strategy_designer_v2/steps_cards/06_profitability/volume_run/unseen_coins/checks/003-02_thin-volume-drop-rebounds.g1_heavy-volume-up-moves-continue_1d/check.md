---
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
data: AAVE, ADA, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI, TAO, TRX, UNI as AAVEUSD, ADAUSD, AVAXUSD, DOGEUSD, INJUSD, LINKUSD, NEARUSD, ONDOUSD, SOLUSD, SUIUSD, TAOUSD, TRXUSD, UNIUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6423 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3514 | above 0 | no |
| Mean daily return, on days in a position | 0.001282 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.453 | above 0 | yes |
| Calmar | 0.4797 | above 0.75 | no |
| Trades per day | 0.1771 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.203 % |
| Yearly return | +13.0 % (over 6.95 years) |
| Days in a position | 32 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/volume_run/unseen_coins/backtests/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
