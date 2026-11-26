---
backtest: 035-01.b1_calm-market-nearness-to-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 2.212 | above 0 | yes |
| Sharpe minus holding's Sharpe | 2.146 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008203 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.014 | above 0 | yes |
| Calmar | 6.565 | above 0.75 | yes |
| Trades per day | 0.152 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.524 % |
| Yearly return | +24.2 % (over 0.87 years) |
| Days in a position | 74 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
