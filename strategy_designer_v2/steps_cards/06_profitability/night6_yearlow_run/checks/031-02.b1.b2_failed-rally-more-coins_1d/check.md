---
backtest: 031-02.b1.b2_failed-rally-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8983 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3178 | above 0 | yes |
| Mean daily return, on days in a position | 0.0003581 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.628 | above 0 | yes |
| Calmar | 0.5816 | above 0.75 | no |
| Trades per day | 0.01861 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.474 % |
| Yearly return | +8.0 % (over 7.94 years) |
| Days in a position | 62 % of the coins' days |

- Decided by: failed: Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1.b2_failed-rally-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
