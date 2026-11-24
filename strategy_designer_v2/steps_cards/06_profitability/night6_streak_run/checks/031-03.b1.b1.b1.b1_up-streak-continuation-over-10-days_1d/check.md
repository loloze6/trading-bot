---
backtest: 031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9602 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3797 | above 0 | yes |
| Mean daily return, on days in a position | 0.001984 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7702 | above 0 | yes |
| Calmar | 0.7542 | above 0.75 | yes |
| Trades per day | 0.06385 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.589 % |
| Yearly return | +42.2 % (over 7.94 years) |
| Days in a position | 66 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
