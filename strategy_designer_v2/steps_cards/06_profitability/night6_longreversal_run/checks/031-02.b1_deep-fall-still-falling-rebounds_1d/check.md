---
backtest: 031-02.b1_deep-fall-still-falling-rebounds_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7421 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.2093 | above 0 | yes |
| Mean daily return, on days in a position | 0.001833 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.5222 | above 0 | yes |
| Calmar | 0.4143 | above 0.75 | no |
| Trades per day | 0.01058 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.902 % |
| Yearly return | +12.0 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1_deep-fall-still-falling-rebounds_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
