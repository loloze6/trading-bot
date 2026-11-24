---
backtest: 031-01.b1_near-yearly-low-falls-all-coins_1d
data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; folds A, B, C, D
status: not profitable enough
---
| Measure | Value | Rule | Passed |
|---|---|---|---|
| Sharpe | -0.2834 | above 0 | no |
| Sharpe minus holding's Sharpe | -0.8639 | above 0 | no |
| Mean daily return, on days in a position | -0.0003301 | at least 0.0005 | no |
| Lowest Sharpe, one window left out | -0.4913 | above 0 | no |
| Calmar | -0.1791 | above 0.75 | no |
| Trades per day | 0.06927 | at least 0.01 | yes |

| Informative measure | Value |
|---|---|
| Daily standard deviation | 1.921 % |
| Yearly return | -15.7 % (over 7.94 years) |
| Days in a position | 86 % of the coins' days |

- Decided by: failed: Sharpe; Sharpe minus holding's Sharpe; Mean daily return, on days in a position; Lowest Sharpe, one window left out; Calmar
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.b1_near-yearly-low-falls-all-coins_1d`
Rule: `steps_cards/06_profitability/helper/rule.yaml`
