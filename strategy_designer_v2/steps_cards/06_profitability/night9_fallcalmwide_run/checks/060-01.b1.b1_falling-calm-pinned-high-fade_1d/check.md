---
backtest: 060-01.b1.b1_falling-calm-pinned-high-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.272 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2808 | above 0 | no |
| Mean daily return, on days in a position | 0.0003988 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.05712 | above 0 | yes |
| Calmar | 0.1619 | above 0.75 | no |
| Trades per day | 0.00375 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.021 % |
| Yearly return | +0.1 % (over 7.94 years) |
| Days in a position | 1 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar; Trades per day
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/060-01.b1.b1_falling-calm-pinned-high-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
