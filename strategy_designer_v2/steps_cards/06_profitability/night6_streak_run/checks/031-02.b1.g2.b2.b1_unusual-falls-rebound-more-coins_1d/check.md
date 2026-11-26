---
backtest: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.6224 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.02197 | above 0 | yes |
| Mean daily return, on days in a position | 0.0006902 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.4883 | above 0 | yes |
| Calmar | 0.4412 | above 0.75 | no |
| Trades per day | 0.5148 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.758 % |
| Yearly return | +16.4 % (over 7.94 years) |
| Days in a position | 83 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
