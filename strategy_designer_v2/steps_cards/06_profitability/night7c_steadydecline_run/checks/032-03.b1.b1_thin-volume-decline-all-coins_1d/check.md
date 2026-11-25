---
backtest: 032-03.b1.b1_thin-volume-decline-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.1963 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.3994 | above 0 | no |
| Mean daily return, on days in a position | 0.0001722 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | 0.06173 | above 0 | yes |
| Calmar | 0.05301 | above 0.75 | no |
| Trades per day | 0.1309 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.070 % |
| Yearly return | +2.0 % (over 7.94 years) |
| Days in a position | 64 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Calmar
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b1.b1_thin-volume-decline-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
