---
backtest: 067-02.b1.b1.d3_calm-choppy-month-rise-continues_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7233 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1705 | above 0 | yes |
| Mean daily return, on days in a position | 0.0008473 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5743 | above 0 | yes |
| Calmar | 0.5054 | above 0.75 | no |
| Trades per day | 0.08194 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.612 % |
| Yearly return | +8.1 % (over 7.94 years) |
| Days in a position | 27 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d3_calm-choppy-month-rise-continues_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
