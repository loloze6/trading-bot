---
backtest: 034-01.b1_nearness-to-high-10-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 3.06 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.6915 | above 0 | no |
| Mean daily return, on days in a position | 0.002594 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 2.671 | above 0 | yes |
| Calmar | 5.601 | above 0.75 | yes |
| Trades per day | 0.1395 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.287 % |
| Yearly return | +105.8 % (over 1.99 years) |
| Days in a position | 79 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/034-01.b1_nearness-to-high-10-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
