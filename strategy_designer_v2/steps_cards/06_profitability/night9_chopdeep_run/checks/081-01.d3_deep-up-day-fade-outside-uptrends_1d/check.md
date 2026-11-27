---
backtest: 081-01.d3_deep-up-day-fade-outside-uptrends_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.4791 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1284 | above 0 | no |
| Mean daily return, on days in a position | 0.0006008 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3349 | above 0 | yes |
| Calmar | 0.2645 | above 0.75 | no |
| Trades per day | 0.179 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.891 % |
| Yearly return | +7.0 % (over 7.94 years) |
| Days in a position | 37 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/081-01.d3_deep-up-day-fade-outside-uptrends_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
