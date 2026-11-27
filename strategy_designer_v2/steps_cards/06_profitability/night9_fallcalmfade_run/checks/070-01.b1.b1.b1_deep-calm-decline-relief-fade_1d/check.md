---
backtest: 070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.02 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4677 | above 0 | yes |
| Mean daily return, on days in a position | 0.004297 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7707 | above 0 | yes |
| Calmar | 1.283 | above 0.75 | yes |
| Trades per day | 0.0101 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.167 % |
| Yearly return | +3.3 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.b1.b1.b1_deep-calm-decline-relief-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
