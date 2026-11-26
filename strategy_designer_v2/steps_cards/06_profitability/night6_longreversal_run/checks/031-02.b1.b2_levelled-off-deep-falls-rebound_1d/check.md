---
backtest: 031-02.b1.b2_levelled-off-deep-falls-rebound_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1816 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.7508 | above 0 | no |
| Mean daily return, on days in a position | -0.0001829 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3159 | above 0 | no |
| Calmar | -0.05778 | above 0.75 | no |
| Trades per day | 0.00138 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.060 % |
| Yearly return | -0.2 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1.b2_levelled-off-deep-falls-rebound_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
