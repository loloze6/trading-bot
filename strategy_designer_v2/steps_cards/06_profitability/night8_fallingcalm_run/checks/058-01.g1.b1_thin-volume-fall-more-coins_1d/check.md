---
backtest: 058-01.g1.b1_thin-volume-fall-more-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.3559 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.1919 | above 0 | no |
| Mean daily return, on days in a position | 0.0006379 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.1493 | above 0 | yes |
| Calmar | 0.2134 | above 0.75 | no |
| Trades per day | 0.0634 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.663 % |
| Yearly return | +3.8 % (over 7.94 years) |
| Days in a position | 19 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Calmar
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.g1.b1_thin-volume-fall-more-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
