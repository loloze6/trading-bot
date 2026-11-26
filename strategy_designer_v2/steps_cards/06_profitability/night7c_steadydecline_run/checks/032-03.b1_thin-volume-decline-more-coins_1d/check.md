---
backtest: 032-03.b1_thin-volume-decline-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.0988 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5069 | above 0 | no |
| Mean daily return, on days in a position | 0.0001021 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.07733 | above 0 | no |
| Calmar | 0.004565 | above 0.75 | no |
| Trades per day | 0.08175 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.931 % |
| Yearly return | +0.2 % (over 7.94 years) |
| Days in a position | 47 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b1_thin-volume-decline-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
