---
backtest: 035-01.b1_calm-market-nearness-to-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.863 | above 0 | yes |
| Sharpe minus holding's Sharpe | -1.327 | above 0 | no |
| Mean daily return, on days in a position | 0.001461 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.475 | above 0 | yes |
| Calmar | 2.392 | above 0.75 | yes |
| Trades per day | 0.121 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.699 % |
| Yearly return | +27.1 % (over 1.99 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
