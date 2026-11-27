---
backtest: 064-01.g1.b1.b1_calm-decline-fade-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1213 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6741 | above 0 | no |
| Mean daily return, on days in a position | -0.0004546 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.3336 | above 0 | no |
| Calmar | -0.05913 | above 0.75 | no |
| Trades per day | 0.02058 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.293 % |
| Yearly return | -0.8 % (over 7.94 years) |
| Days in a position | 4 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01.g1.b1.b1_calm-decline-fade-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
