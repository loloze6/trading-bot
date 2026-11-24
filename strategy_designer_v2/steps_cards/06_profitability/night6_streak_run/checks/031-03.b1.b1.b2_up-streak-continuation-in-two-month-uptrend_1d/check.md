---
backtest: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8067 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2262 | above 0 | yes |
| Mean daily return, on days in a position | 0.001999 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5986 | above 0 | yes |
| Calmar | 0.4599 | above 0.75 | no |
| Trades per day | 0.02714 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.759 % |
| Yearly return | +32.6 % (over 7.94 years) |
| Days in a position | 58 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
