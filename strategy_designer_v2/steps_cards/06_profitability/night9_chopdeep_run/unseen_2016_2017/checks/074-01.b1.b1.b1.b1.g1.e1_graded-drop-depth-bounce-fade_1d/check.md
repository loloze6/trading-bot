---
backtest: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2016_2017
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.6553 | above 0 | no |
| Sharpe minus holding's Sharpe | -4.406 | above 0 | no |
| Mean daily return, on days in a position | -0.00322 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -1.489 | above 0 | no |
| Calmar | -0.3427 | above 0.75 | no |
| Trades per day | 0.01026 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.183 % |
| Yearly return | -2.3 % (over 1.99 years) |
| Days in a position | 2 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
