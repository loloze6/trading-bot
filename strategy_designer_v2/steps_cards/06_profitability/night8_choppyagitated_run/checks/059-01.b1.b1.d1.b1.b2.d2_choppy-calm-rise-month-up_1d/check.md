---
backtest: 059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6895 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1367 | above 0 | yes |
| Mean daily return, on days in a position | 0.001661 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5294 | above 0 | yes |
| Calmar | 0.3745 | above 0.75 | no |
| Trades per day | 0.03558 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.606 % |
| Yearly return | +7.6 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
