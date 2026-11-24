---
backtest: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8707 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8044 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008394 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1812 | above 0 | yes |
| Calmar | 1.374 | above 0.75 | yes |
| Trades per day | 0.1363 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.417 % |
| Yearly return | +22.1 % (over 0.87 years) |
| Days in a position | 77 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
