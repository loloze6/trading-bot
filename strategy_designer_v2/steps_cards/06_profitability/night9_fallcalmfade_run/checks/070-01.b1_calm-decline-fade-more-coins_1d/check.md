---
backtest: 070-01.b1_calm-decline-fade-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.1049 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.6577 | above 0 | no |
| Mean daily return, on days in a position | -0.0002207 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4555 | above 0 | no |
| Calmar | -0.05292 | above 0.75 | no |
| Trades per day | 0.05023 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.410 % |
| Yearly return | -1.1 % (over 7.94 years) |
| Days in a position | 10 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.b1_calm-decline-fade-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
