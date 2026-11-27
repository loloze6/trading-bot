---
backtest: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.9427 | above 0 | yes |
| Sharpe minus holding's Sharpe | 0.3352 | above 0 | yes |
| Mean daily return, on days in a position | 0.006083 | at least 0.0005 | yes |
| Lowest Sharpe, one window left out | 0.7341 | above 0 | yes |
| Calmar | 1.13 | above 0.75 | yes |
| Trades per day | 0.01479 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 0.367 % |
| Yearly return | +6.6 % (over 7.94 years) |
| Days in a position | 3 % of the coins' days |

- Decided by: every measure passed
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
