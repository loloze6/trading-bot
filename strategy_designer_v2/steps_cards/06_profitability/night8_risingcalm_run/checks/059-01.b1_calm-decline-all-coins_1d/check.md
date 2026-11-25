---
backtest: 059-01.b1_calm-decline-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | 0.03069 | above 0 | yes |
| Sharpe minus holding's Sharpe | -0.5221 | above 0 | no |
| Mean daily return, on days in a position | 4.747e-05 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.08186 | above 0 | no |
| Calmar | -0.03496 | above 0.75 | no |
| Trades per day | 0.1535 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.009 % |
| Yearly return | -1.2 % (over 7.94 years) |
| Days in a position | 34 % of the coins' days |

- Decided by: failed: Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-01.b1_calm-decline-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
