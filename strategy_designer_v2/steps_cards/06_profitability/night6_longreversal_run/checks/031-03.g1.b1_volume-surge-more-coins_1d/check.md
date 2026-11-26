---
backtest: 031-03.g1.b1_volume-surge-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5663 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04116 | above 0 | no |
| Mean daily return, on days in a position | 0.0004268 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.4184 | above 0 | yes |
| Calmar | 0.2352 | above 0.75 | no |
| Trades per day | 0.2983 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.436 % |
| Yearly return | +12.5 % (over 7.94 years) |
| Days in a position | 100 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1_volume-surge-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
