---
backtest: 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1651 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.09876 | above 0 | yes |
| Mean daily return, on days in a position | 0.0002895 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.06822 | above 0 | no |
| Calmar | 0.05452 | above 0.75 | no |
| Trades per day | 0.05804 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.297 % |
| Yearly return | +1.1 % (over 0.87 years) |
| Days in a position | 39 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_streak_run/unseen_2026/backtests/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
