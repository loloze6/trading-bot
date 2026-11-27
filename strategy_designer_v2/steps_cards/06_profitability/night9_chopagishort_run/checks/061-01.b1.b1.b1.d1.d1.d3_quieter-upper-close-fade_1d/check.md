---
backtest: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.2997 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.2531 | above 0 | no |
| Mean daily return, on days in a position | 0.001579 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | -0.01711 | above 0 | no |
| Calmar | 0.4167 | above 0.75 | no |
| Trades per day | 0.01534 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.504 % |
| Yearly return | +2.5 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
