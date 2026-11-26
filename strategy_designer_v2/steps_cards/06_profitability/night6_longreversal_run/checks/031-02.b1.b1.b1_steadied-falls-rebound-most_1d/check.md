---
backtest: 031-02.b1.b1.b1_steadied-falls-rebound-most_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.4357 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.027 | above 0 | no |
| Mean daily return, on days in a position | -0.0007498 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6407 | above 0 | no |
| Calmar | -0.1184 | above 0.75 | no |
| Trades per day | 0.02136 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.751 % |
| Yearly return | -7.0 % (over 7.94 years) |
| Days in a position | 23 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1.b1.b1_steadied-falls-rebound-most_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
