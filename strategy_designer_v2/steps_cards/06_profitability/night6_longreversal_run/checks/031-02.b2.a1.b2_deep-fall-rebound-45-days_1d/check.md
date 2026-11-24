---
backtest: 031-02.b2.a1.b2_deep-fall-rebound-45-days_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.528 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01809 | above 0 | yes |
| Mean daily return, on days in a position | 0.000619 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3288 | above 0 | yes |
| Calmar | 0.2504 | above 0.75 | no |
| Trades per day | 0.02941 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.446 % |
| Yearly return | +11.4 % (over 7.94 years) |
| Days in a position | 65 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b2.a1.b2_deep-fall-rebound-45-days_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
