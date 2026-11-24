---
backtest: 031-03.g1.b1.g2_swelling-volume-after-rises_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.112 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.5048 | above 0 | yes |
| Mean daily return, on days in a position | 0.00128 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.9014 | above 0 | yes |
| Calmar | 1.049 | above 0.75 | yes |
| Trades per day | 0.0911 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.287 % |
| Yearly return | +27.5 % (over 7.94 years) |
| Days in a position | 59 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.g2_swelling-volume-after-rises_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
