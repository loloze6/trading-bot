---
backtest: 031-02.b1.b1_deepest-falls-rebound-most_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7101 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1773 | above 0 | yes |
| Mean daily return, on days in a position | 0.001606 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5297 | above 0 | yes |
| Calmar | 0.391 | above 0.75 | no |
| Trades per day | 0.0112 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.930 % |
| Yearly return | +11.7 % (over 7.94 years) |
| Days in a position | 22 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1.b1_deepest-falls-rebound-most_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
