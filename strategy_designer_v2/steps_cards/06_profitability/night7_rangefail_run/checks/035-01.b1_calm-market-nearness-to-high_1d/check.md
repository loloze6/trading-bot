---
backtest: 035-01.b1_calm-market-nearness-to-high_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 1.188 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.6357 | above 0 | yes |
| Mean daily return, on days in a position | 0.0005163 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 1.034 | above 0 | yes |
| Calmar | 0.8655 | above 0.75 | yes |
| Trades per day | 0.1415 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.548 % |
| Yearly return | +12.6 % (over 7.94 years) |
| Days in a position | 66 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
