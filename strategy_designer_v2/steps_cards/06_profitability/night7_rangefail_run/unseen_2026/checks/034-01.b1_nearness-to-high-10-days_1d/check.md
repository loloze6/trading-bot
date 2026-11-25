---
backtest: 034-01.b1_nearness-to-high-10-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9193 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.8529 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005073 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1369 | above 0 | yes |
| Calmar | 2.092 | above 0.75 | yes |
| Trades per day | 0.06526 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.443 % |
| Yearly return | +7.7 % (over 0.87 years) |
| Days in a position | 42 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/034-01.b1_nearness-to-high-10-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
