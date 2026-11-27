---
backtest: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1705 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3823 | above 0 | no |
| Mean daily return, on days in a position | 0.0002668 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.01135 | above 0 | yes |
| Calmar | 0.03874 | above 0.75 | no |
| Trades per day | 0.07375 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.934 % |
| Yearly return | +1.4 % (over 7.94 years) |
| Days in a position | 31 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
