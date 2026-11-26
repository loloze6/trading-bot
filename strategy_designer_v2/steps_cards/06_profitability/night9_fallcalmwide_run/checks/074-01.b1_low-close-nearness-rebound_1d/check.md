---
backtest: 074-01.b1_low-close-nearness-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.049 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4958 | above 0 | yes |
| Mean daily return, on days in a position | 0.004697 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9306 | above 0 | yes |
| Calmar | 1.156 | above 0.75 | yes |
| Trades per day | 0.009452 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.161 % |
| Yearly return | +3.2 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Trades per day
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b1_low-close-nearness-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
