---
backtest: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.5358 | above 0 | no |
| Sharpe minus holding's Sharpe | -1.143 | above 0 | no |
| Mean daily return, on days in a position | -0.001999 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.5948 | above 0 | no |
| Calmar | -0.7801 | above 0.75 | no |
| Trades per day | 0.05277 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 2.689 % |
| Yearly return | -100.0 % (over 7.94 years) |
| Days in a position | 38 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
