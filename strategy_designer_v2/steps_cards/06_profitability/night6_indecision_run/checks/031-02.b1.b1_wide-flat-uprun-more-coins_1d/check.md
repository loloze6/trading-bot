---
backtest: 031-02.b1.b1_wide-flat-uprun-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.7983 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.1908 | above 0 | yes |
| Mean daily return, on days in a position | 0.002104 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6546 | above 0 | yes |
| Calmar | 0.6458 | above 0.75 | no |
| Trades per day | 0.008348 | at least 0.01 | no |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.385 % |
| Yearly return | +5.8 % (over 7.94 years) |
| Days in a position | 8 % of the coins' days |

- Decided by: failed: Calmar; Trades per day
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1_wide-flat-uprun-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
