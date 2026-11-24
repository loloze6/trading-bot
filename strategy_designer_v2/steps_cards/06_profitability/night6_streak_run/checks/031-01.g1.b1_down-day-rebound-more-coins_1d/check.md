---
backtest: 031-01.g1.b1_down-day-rebound-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4806 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1198 | above 0 | no |
| Mean daily return, on days in a position | 0.0005814 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3118 | above 0 | yes |
| Calmar | 0.2288 | above 0.75 | no |
| Trades per day | 0.4847 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.076 % |
| Yearly return | +11.7 % (over 7.94 years) |
| Days in a position | 90 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.g1.b1_down-day-rebound-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
