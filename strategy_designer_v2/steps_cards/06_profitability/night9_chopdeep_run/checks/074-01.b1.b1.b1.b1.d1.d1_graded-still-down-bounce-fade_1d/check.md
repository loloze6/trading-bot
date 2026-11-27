---
backtest: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7276 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1201 | above 0 | yes |
| Mean daily return, on days in a position | 0.001237 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4855 | above 0 | yes |
| Calmar | 0.7971 | above 0.75 | yes |
| Trades per day | 0.07304 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.475 % |
| Yearly return | +6.4 % (over 7.94 years) |
| Days in a position | 15 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
