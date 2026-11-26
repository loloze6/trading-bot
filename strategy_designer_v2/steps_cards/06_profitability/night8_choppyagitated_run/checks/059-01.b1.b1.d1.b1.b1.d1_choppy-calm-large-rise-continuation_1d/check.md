---
backtest: 059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.5128 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.03994 | above 0 | no |
| Mean daily return, on days in a position | 0.001294 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.2841 | above 0 | yes |
| Calmar | 0.2256 | above 0.75 | no |
| Trades per day | 0.03455 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.171 % |
| Yearly return | +9.4 % (over 7.94 years) |
| Days in a position | 24 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
