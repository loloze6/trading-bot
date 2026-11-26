---
backtest: 059-01.b1.b1.d1_choppy-calm-swing-scaled-rise_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.569 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.01619 | above 0 | yes |
| Mean daily return, on days in a position | 0.001747 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.3295 | above 0 | yes |
| Calmar | 0.2546 | above 0.75 | no |
| Trades per day | 0.02665 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.076 % |
| Yearly return | +10.0 % (over 7.94 years) |
| Days in a position | 18 % of the coins' days |

- Decided by: failed: Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1_choppy-calm-swing-scaled-rise_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
