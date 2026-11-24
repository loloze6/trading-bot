---
backtest: 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.722 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.059 | above 0 | no |
| Mean daily return, on days in a position | 0.006641 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.393 | above 0 | yes |
| Calmar | 6.38 | above 0.75 | yes |
| Trades per day | 0.07632 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.624 % |
| Yearly return | +246.5 % (over 1.99 years) |
| Days in a position | 56 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2016_2017/backtests/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
