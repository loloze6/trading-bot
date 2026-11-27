---
backtest: 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8843 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2768 | above 0 | yes |
| Mean daily return, on days in a position | 0.001941 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7008 | above 0 | yes |
| Calmar | 1.219 | above 0.75 | yes |
| Trades per day | 0.06727 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.537 % |
| Yearly return | +8.9 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
