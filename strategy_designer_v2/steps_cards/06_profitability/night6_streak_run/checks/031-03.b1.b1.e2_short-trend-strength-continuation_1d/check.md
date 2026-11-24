---
backtest: 031-03.b1.b1.e2_short-trend-strength-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.054 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.4532 | above 0 | yes |
| Mean daily return, on days in a position | 0.001174 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.8388 | above 0 | yes |
| Calmar | 1.146 | above 0.75 | yes |
| Trades per day | 0.2409 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.560 % |
| Yearly return | +31.0 % (over 7.94 years) |
| Days in a position | 73 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-03.b1.b1.e2_short-trend-strength-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
