---
backtest: 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.8485 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.241 | above 0 | yes |
| Mean daily return, on days in a position | 0.00318 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.6212 | above 0 | yes |
| Calmar | 0.9673 | above 0.75 | yes |
| Trades per day | 0.02711 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.383 % |
| Yearly return | +6.1 % (over 7.94 years) |
| Days in a position | 5 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
