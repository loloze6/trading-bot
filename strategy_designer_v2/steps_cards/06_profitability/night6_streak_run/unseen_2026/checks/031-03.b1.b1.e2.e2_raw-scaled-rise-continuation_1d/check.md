---
backtest: 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4598 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3934 | above 0 | yes |
| Mean daily return, on days in a position | 0.001546 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.1822 | above 0 | no |
| Calmar | 0.8558 | above 0.75 | yes |
| Trades per day | 0.01787 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.616 % |
| Yearly return | +4.8 % (over 0.87 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Lowest Sharpe, one window left out
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
