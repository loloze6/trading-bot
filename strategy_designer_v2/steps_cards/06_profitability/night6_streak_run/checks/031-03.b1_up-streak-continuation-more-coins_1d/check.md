---
backtest: 031-03.b1_up-streak-continuation-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6143 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.03381 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008977 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4438 | above 0 | yes |
| Calmar | 0.3281 | above 0.75 | no |
| Trades per day | 0.2657 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.697 % |
| Yearly return | +20.1 % (over 7.94 years) |
| Days in a position | 97 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1_up-streak-continuation-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
