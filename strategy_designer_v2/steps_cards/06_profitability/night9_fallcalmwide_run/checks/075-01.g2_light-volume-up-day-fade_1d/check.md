---
backtest: 075-01.g2_light-volume-up-day-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3875 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.9949 | above 0 | no |
| Mean daily return, on days in a position | -0.0002286 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5581 | above 0 | no |
| Calmar | -0.1333 | above 0.75 | no |
| Trades per day | 0.2394 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.515 % |
| Yearly return | -4.2 % (over 7.94 years) |
| Days in a position | 46 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.g2_light-volume-up-day-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
