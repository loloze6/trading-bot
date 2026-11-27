---
backtest: 077-03.g1_choppy-agitated-high-close-fall_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5215 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03128 | above 0 | no |
| Mean daily return, on days in a position | 0.001365 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.447 | above 0 | yes |
| Calmar | 0.3854 | above 0.75 | no |
| Trades per day | 0.01763 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.172 % |
| Yearly return | +1.7 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.g1_choppy-agitated-high-close-fall_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
