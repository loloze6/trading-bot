---
backtest: 061-01_falling-calm-rally-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.3902 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.943 | above 0 | no |
| Mean daily return, on days in a position | -0.000647 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.6108 | above 0 | no |
| Calmar | -0.1303 | above 0.75 | no |
| Trades per day | 0.07599 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.421 % |
| Yearly return | -3.4 % (over 7.94 years) |
| Days in a position | 13 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/061-01_falling-calm-rally-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
