---
backtest: 077-01.b1.b1_graded-swing-rise-carries-on_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3475 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2053 | above 0 | no |
| Mean daily return, on days in a position | 0.0008023 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1636 | above 0 | yes |
| Calmar | 0.1388 | above 0.75 | no |
| Trades per day | 0.0498 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.787 % |
| Yearly return | +4.2 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1.b1_graded-swing-rise-carries-on_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
