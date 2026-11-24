---
backtest: 031-04.a1_yearly-low-break-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5362 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.04427 | above 0 | no |
| Mean daily return, on days in a position | 0.0009359 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3585 | above 0 | yes |
| Calmar | 0.5495 | above 0.75 | no |
| Trades per day | 0.000856 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.054 % |
| Yearly return | +0.6 % (over 7.94 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-04.a1_yearly-low-break-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
