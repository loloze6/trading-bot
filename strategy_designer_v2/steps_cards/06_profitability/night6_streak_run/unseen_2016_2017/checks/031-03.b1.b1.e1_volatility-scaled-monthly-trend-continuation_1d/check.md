---
backtest: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.139 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6422 | above 0 | no |
| Mean daily return, on days in a position | 0.005188 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.716 | above 0 | yes |
| Calmar | 11.47 | above 0.75 | yes |
| Trades per day | 0.1769 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.792 % |
| Yearly return | +364.7 % (over 1.99 years) |
| Days in a position | 88 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2016_2017/backtests/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
