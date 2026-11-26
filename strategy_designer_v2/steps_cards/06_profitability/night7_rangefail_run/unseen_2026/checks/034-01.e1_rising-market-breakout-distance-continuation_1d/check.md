---
backtest: 034-01.e1_rising-market-breakout-distance-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.817 | above 0 | yes |
| Sharpe minus holding's Sharpe | 1.75 | above 0 | yes |
| Mean daily return, on days in a position | 0.002161 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7606 | above 0 | yes |
| Calmar | 7.826 | above 0.75 | yes |
| Trades per day | 0.03951 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.346 % |
| Yearly return | +12.5 % (over 0.87 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/034-01.e1_rising-market-breakout-distance-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
