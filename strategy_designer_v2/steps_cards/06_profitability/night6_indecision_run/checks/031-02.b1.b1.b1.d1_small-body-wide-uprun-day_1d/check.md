---
backtest: 031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.263 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6551 | above 0 | yes |
| Mean daily return, on days in a position | 0.002894 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.084 | above 0 | yes |
| Calmar | 0.9545 | above 0.75 | yes |
| Trades per day | 0.04883 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.602 % |
| Yearly return | +14.9 % (over 7.94 years) |
| Days in a position | 14 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
